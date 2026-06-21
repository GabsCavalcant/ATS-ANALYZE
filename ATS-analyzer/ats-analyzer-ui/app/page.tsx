"use client"

import { useState } from "react"
import { AppHeader } from "@/components/app-header"
import { ResumeDropzone } from "@/components/resume-dropzone"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Textarea } from "@/components/ui/textarea"
import { Button } from "@/components/ui/button"
import { Sparkles } from "lucide-react"

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://127.0.0.1:8000/analyze"

export default function Page() {
  const [jobDescription, setJobDescription] = useState("")
  const [resumeFile, setResumeFile] = useState<File | null>(null)
  const [result, setResult] = useState<any>(null)
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)

  async function handleAnalyze() {
    setError(null)
    setResult(null)

    if (!jobDescription.trim()) {
      setError("Digite a descrição da vaga para continuar.")
      return
    }

    if (!resumeFile) {
      setError("Selecione um currículo em PDF.")
      return
    }

    setLoading(true)

    const formData = new FormData()
    formData.append("job_description", jobDescription)
    formData.append("resume", resumeFile)

    try {
      const response = await fetch(API_URL, {
        method: "POST",
        mode: "cors",
        body: formData,
      })

      if (!response.ok) {
        const body = await response.json().catch(() => null)
        throw new Error(body?.detail ?? "Erro ao conectar com o backend.")
      }

      const data = await response.json()
      setResult(data)
    } catch (err) {
      setError(err instanceof Error ? err.message : String(err))
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="min-h-screen bg-background text-foreground">
      <AppHeader />

      <div className="mx-auto max-w-6xl px-4 py-8 sm:px-6 sm:py-10">
        <div className="grid grid-cols-1 gap-6 lg:grid-cols-5">
          <Card className="rounded-xl shadow-sm lg:col-span-3">
            <CardHeader>
              <CardTitle className="text-base font-semibold">Job Description</CardTitle>
            </CardHeader>
            <CardContent>
              <Textarea
                id="job-description"
                value={jobDescription}
                onChange={(event) => setJobDescription(event.target.value)}
                placeholder="Cole aqui o texto completo da vaga..."
                className="min-h-80 resize-y rounded-lg text-sm leading-relaxed"
                aria-label="Job Description"
              />
            </CardContent>
          </Card>

          <Card className="rounded-xl shadow-sm lg:col-span-2">
            <CardHeader>
              <CardTitle className="text-base font-semibold">Upload Resume (PDF)</CardTitle>
            </CardHeader>
            <CardContent>
              <ResumeDropzone file={resumeFile} onFileChange={setResumeFile} />
            </CardContent>
          </Card>
        </div>

        <div className="mt-8 flex flex-col items-center gap-4">
          {error ? (
            <div className="rounded-xl border border-destructive/30 bg-destructive/5 px-4 py-3 text-sm text-destructive">
              {error}
            </div>
          ) : null}

          <Button
            size="lg"
            onClick={handleAnalyze}
            disabled={loading}
            className="min-w-48 gap-2 rounded-xl bg-primary px-10 text-base font-bold text-primary-foreground shadow-sm transition-colors hover:bg-primary/90"
          >
            <Sparkles className="h-5 w-5" aria-hidden="true" />
            {loading ? "Analisando..." : "Analyze"}
          </Button>
        </div>

        {result ? (
          <section className="mt-10 space-y-4 rounded-3xl border border-border bg-muted p-6">
            <h2 className="text-xl font-semibold">Resultado da análise</h2>
            <div className="grid gap-4 sm:grid-cols-2">
              <div className="rounded-xl bg-background p-4 shadow-sm">
                <p className="text-sm font-medium text-muted-foreground">Match rate</p>
                <p className="mt-2 text-3xl font-bold text-foreground">
                  {result.match.skills.match_rate != null
                    ? `${Math.round(result.match.skills.match_rate * 100)}%`
                    : "-"}
                </p>
              </div>
              <div className="rounded-xl bg-background p-4 shadow-sm">
                <p className="text-sm font-medium text-muted-foreground">Skills encontradas</p>
                <p className="mt-2 text-sm text-foreground">
                  {result.match.skills.matched.length} correspondências, {result.match.skills.missing.length} faltantes
                </p>
              </div>
            </div>

            <div className="grid gap-4 md:grid-cols-2">
              <div className="rounded-xl bg-background p-4 shadow-sm">
                <h3 className="text-sm font-semibold">Skills compatíveis</h3>
                <p className="mt-2 text-sm text-foreground">
                  {result.match.skills.matched.join(", ") || "Nenhuma"}
                </p>
              </div>
              <div className="rounded-xl bg-background p-4 shadow-sm">
                <h3 className="text-sm font-semibold">Skills faltantes</h3>
                <p className="mt-2 text-sm text-foreground">
                  {result.match.skills.missing.join(", ") || "Nenhuma"}
                </p>
              </div>
            </div>
          </section>
        ) : null}
      </div>
    </main>
  )
}
