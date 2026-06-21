"use client"

import type React from "react"

import { useRef, useState } from "react"
import { UploadCloud, FileText, X } from "lucide-react"
import { cn } from "@/lib/utils"

interface ResumeDropzoneProps {
  file: File | null
  onFileChange: (file: File | null) => void
}

export function ResumeDropzone({ file, onFileChange }: ResumeDropzoneProps) {
  const inputRef = useRef<HTMLInputElement>(null)
  const [isDragging, setIsDragging] = useState(false)

  function handleFiles(files: FileList | null) {
    const selected = files?.[0]
    if (selected && selected.type === "application/pdf") {
      onFileChange(selected)
      return
    }

    onFileChange(null)
  }

  function handleDrop(e: React.DragEvent<HTMLDivElement>) {
    e.preventDefault()
    setIsDragging(false)
    handleFiles(e.dataTransfer.files)
  }

  function clearFile(e: React.MouseEvent) {
    e.stopPropagation()
    onFileChange(null)
    if (inputRef.current) inputRef.current.value = ""
  }

  return (
    <div
      role="button"
      tabIndex={0}
      aria-label="Upload Resume (PDF)"
      onClick={() => inputRef.current?.click()}
      onKeyDown={(e) => {
        if (e.key === "Enter" || e.key === " ") {
          e.preventDefault()
          inputRef.current?.click()
        }
      }}
      onDragOver={(e) => {
        e.preventDefault()
        setIsDragging(true)
      }}
      onDragLeave={() => setIsDragging(false)}
      onDrop={handleDrop}
      className={cn(
        "flex min-h-64 cursor-pointer flex-col items-center justify-center rounded-xl border-2 border-dashed p-6 text-center transition-colors",
        "border-border bg-muted/40 hover:border-primary hover:bg-accent",
        isDragging && "border-primary bg-accent",
      )}
    >
      <input
        ref={inputRef}
        type="file"
        accept="application/pdf"
        className="sr-only"
        onChange={(e) => handleFiles(e.target.files)}
      />

      {file ? (
        <div className="flex flex-col items-center gap-3">
          <div className="flex h-12 w-12 items-center justify-center rounded-full bg-primary/10 text-primary">
            <FileText className="h-6 w-6" aria-hidden="true" />
          </div>
          <p className="max-w-full truncate text-sm font-medium text-foreground">{file.name}</p>
          <button
            type="button"
            onClick={clearFile}
            className="inline-flex items-center gap-1 text-xs font-medium text-muted-foreground hover:text-foreground"
          >
            <X className="h-3.5 w-3.5" aria-hidden="true" />
            Remover
          </button>
        </div>
      ) : (
        <div className="flex flex-col items-center gap-3">
          <div className="flex h-14 w-14 items-center justify-center rounded-full bg-primary/10 text-primary">
            <UploadCloud className="h-7 w-7" aria-hidden="true" />
          </div>
          <p className="text-sm font-medium text-foreground text-balance">
            Drag &amp; drop your PDF here ou clique para selecionar
          </p>
          <p className="text-xs text-muted-foreground">Apenas arquivos PDF</p>
        </div>
      )}
    </div>
  )
}
