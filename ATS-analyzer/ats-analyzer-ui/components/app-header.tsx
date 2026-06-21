import Image from "next/image"

export function AppHeader() {
  return (
    <header className="w-full bg-[#1F2937] text-white">
      <div className="mx-auto flex max-w-6xl items-center gap-3 px-4 py-5 sm:px-6">
        <div className="relative overflow-hidden rounded-xl">
          <Image
            src="/profile.jpg"
            alt="Foto de perfil"
            width={44}
            height={44}
            className="h-11 w-11 object-cover"
          />
        </div>
        <div className="flex flex-col">
          <h1 className="text-xl font-bold leading-tight tracking-tight">
            ATS <span className="text-primary">Analyzer</span>
          </h1>
          <p className="text-sm leading-tight text-gray-300">AI-powered resume screening</p>
        </div>
      </div>
    </header>
  )
}
