import type { Metadata } from "next";
import "./globals.css";
import Sidebar from "@/components/Sidebar";

export const metadata: Metadata = {
  title: "SoftMatterGPT — AI 教学工作台",
  description: "面向软物质课程与实验教学的 AI 教学工作台",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="zh-CN">
      <head>
        <link
          href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500&display=swap"
          rel="stylesheet"
        />
      </head>
      <body className="text-text font-sans antialiased">
        {/* Starry background */}
        <div className="starry-bg" />

        {/* Chemical pattern overlay */}
        <div className="chemical-pattern" />

        {/* Floating chemical decorations */}
        <div className="fixed inset-0 pointer-events-none z-[1] overflow-hidden">
          {/* Benzene ring - top right */}
          <div className="absolute top-[12%] right-[8%] opacity-[0.04]">
            <svg width="80" height="80" viewBox="0 0 80 80">
              <polygon points="40,5 70,22 70,58 40,75 10,58 10,22" fill="none" stroke="white" strokeWidth="1.5"/>
              <circle cx="40" cy="40" r="12" fill="none" stroke="white" strokeWidth="1"/>
            </svg>
          </div>

          {/* Molecule - bottom left */}
          <div className="absolute bottom-[15%] left-[5%] opacity-[0.04]">
            <svg width="100" height="80" viewBox="0 0 100 80">
              <circle cx="20" cy="40" r="8" fill="white"/>
              <circle cx="50" cy="25" r="6" fill="white"/>
              <circle cx="80" cy="45" r="7" fill="white"/>
              <line x1="28" y1="36" x2="44" y2="28" stroke="white" strokeWidth="2"/>
              <line x1="56" y1="28" x2="73" y2="42" stroke="white" strokeWidth="2"/>
            </svg>
          </div>

          {/* Test tube - top left */}
          <div className="absolute top-[35%] left-[3%] opacity-[0.04]">
            <svg width="40" height="80" viewBox="0 0 40 80">
              <rect x="12" y="5" width="16" height="50" rx="8" fill="none" stroke="white" strokeWidth="1.5"/>
              <rect x="8" y="5" width="24" height="6" rx="3" fill="white"/>
              <path d="M12,45 Q20,65 28,45" fill="rgba(99,102,241,0.2)" stroke="none"/>
            </svg>
          </div>

          {/* Flask - bottom right */}
          <div className="absolute bottom-[25%] right-[10%] opacity-[0.04]">
            <svg width="60" height="80" viewBox="0 0 60 80">
              <path d="M20,5 L20,30 L5,65 Q3,75 15,75 L45,75 Q57,75 55,65 L40,30 L40,5" fill="none" stroke="white" strokeWidth="1.5"/>
              <rect x="17" y="2" width="26" height="6" rx="3" fill="white"/>
              <ellipse cx="30" cy="65" rx="18" ry="8" fill="rgba(6,182,212,0.15)"/>
            </svg>
          </div>

          {/* DNA helix - right middle */}
          <div className="absolute top-[55%] right-[3%] opacity-[0.04]">
            <svg width="30" height="100" viewBox="0 0 30 100">
              <path d="M5,5 Q25,25 5,50 Q25,75 5,95" fill="none" stroke="white" strokeWidth="1.5"/>
              <path d="M25,5 Q5,25 25,50 Q5,75 25,95" fill="none" stroke="white" strokeWidth="1.5"/>
              <line x1="10" y1="15" x2="20" y2="15" stroke="white" strokeWidth="1"/>
              <line x1="15" y1="35" x2="15" y2="35" stroke="white" strokeWidth="1"/>
              <line x1="10" y1="55" x2="20" y2="55" stroke="white" strokeWidth="1"/>
              <line x1="15" y1="75" x2="15" y2="75" stroke="white" strokeWidth="1"/>
            </svg>
          </div>

          {/* Atom - center left */}
          <div className="absolute top-[20%] left-[15%] opacity-[0.03]">
            <svg width="60" height="60" viewBox="0 0 60 60">
              <circle cx="30" cy="30" r="4" fill="white"/>
              <ellipse cx="30" cy="30" rx="25" ry="10" fill="none" stroke="white" strokeWidth="1" transform="rotate(0 30 30)"/>
              <ellipse cx="30" cy="30" rx="25" ry="10" fill="none" stroke="white" strokeWidth="1" transform="rotate(60 30 30)"/>
              <ellipse cx="30" cy="30" rx="25" ry="10" fill="none" stroke="white" strokeWidth="1" transform="rotate(120 30 30)"/>
            </svg>
          </div>

          {/* Droplet - bottom center */}
          <div className="absolute bottom-[10%] left-[45%] opacity-[0.03]">
            <svg width="40" height="50" viewBox="0 0 40 50">
              <path d="M20,5 Q5,25 5,35 Q5,45 20,45 Q35,45 35,35 Q35,25 20,5" fill="none" stroke="white" strokeWidth="1.5"/>
              <circle cx="15" cy="30" r="3" fill="rgba(99,102,241,0.2)"/>
            </svg>
          </div>
        </div>

        <Sidebar />
        <main className="ml-[70px] min-h-screen relative z-10">{children}</main>
      </body>
    </html>
  );
}
