import { type ReactNode } from "react";
import { cn } from "@/lib/utils";
import {
  Users,
  type LucideIcon,
} from "lucide-react";

interface Step {
  id: number;
  label: string;
  icon: LucideIcon;
  description: string;
}

const steps: Step[] = [
  {
    id: 1,
    label: "Knowledge Intake",
    icon: Users,
    description: "Select person & data",
  },
];

interface LayoutProps {
  children: ReactNode;
  currentStep: number;
  onStepChange: (step: number) => void;
  maxStep: number;
}

export function Layout({
  children,
  currentStep,
  onStepChange,
  maxStep,
}: LayoutProps) {
  return (
    <div className="flex min-h-svh flex-col">
      {/* Header */}
      <header className="border-b border-border bg-card/50 backdrop-blur-sm sticky top-0 z-50">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-3 sm:px-6 lg:px-8">
          <div className="flex items-center gap-3">
            <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-primary/10 border border-primary/20">
              <span className="text-primary font-semibold text-sm">G</span>
            </div>
            <div>
              <h1 className="text-lg font-semibold text-foreground tracking-tight leading-none">
                Gemellus
              </h1>
              <p className="text-[11px] text-muted-foreground leading-none mt-0.5">
                Knowledge Twin Platform
              </p>
            </div>
          </div>

          {/* Desktop stepper */}
          <nav className="hidden md:flex items-center gap-1">
            {steps.map((step, i) => {
              const Icon = step.icon;
              const isActive = currentStep === step.id;
              const isCompleted = step.id < currentStep;
              const isAccessible = step.id <= maxStep;

              return (
                <div key={step.id} className="flex items-center">
                  {i > 0 && (
                    <div
                      className={cn(
                        "w-8 h-px mx-1",
                        isCompleted ? "bg-primary/50" : "bg-border"
                      )}
                    />
                  )}
                  <button
                    onClick={() => isAccessible && onStepChange(step.id)}
                    disabled={!isAccessible}
                    className={cn(
                      "flex items-center gap-2 rounded-lg px-3 py-2 text-sm transition-all",
                      isActive &&
                      "bg-primary/10 text-primary border border-primary/20",
                      isCompleted &&
                      "text-primary/70 hover:text-primary",
                      !isActive &&
                      !isCompleted &&
                      isAccessible &&
                      "text-muted-foreground hover:text-foreground",
                      !isAccessible &&
                      "text-muted-foreground/40 cursor-not-allowed"
                    )}
                  >
                    <div
                      className={cn(
                        "flex h-7 w-7 items-center justify-center rounded-md text-xs",
                        isActive && "bg-primary text-primary-foreground",
                        isCompleted &&
                        "bg-primary/20 text-primary",
                        !isActive &&
                        !isCompleted &&
                        "bg-secondary text-muted-foreground"
                      )}
                    >
                      {isCompleted ? (
                        <svg
                          className="h-3.5 w-3.5"
                          fill="none"
                          viewBox="0 0 24 24"
                          stroke="currentColor"
                          strokeWidth={2.5}
                        >
                          <path
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            d="M5 13l4 4L19 7"
                          />
                        </svg>
                      ) : (
                        <Icon className="h-3.5 w-3.5" />
                      )}
                    </div>
                    <div className="text-left hidden lg:block">
                      <div className="font-medium leading-none">
                        {step.label}
                      </div>
                      <div className="text-[10px] text-muted-foreground mt-0.5 leading-none">
                        {step.description}
                      </div>
                    </div>
                  </button>
                </div>
              );
            })}
          </nav>

          <div className="text-xs text-muted-foreground hidden sm:block">
            Step {currentStep} of 3
          </div>
        </div>

        {/* Mobile stepper */}
        <div className="md:hidden border-t border-border">
          <div className="flex">
            {steps.map((step) => {
              const isActive = currentStep === step.id;
              const isCompleted = step.id < currentStep;
              const isAccessible = step.id <= maxStep;

              return (
                <button
                  key={step.id}
                  onClick={() => isAccessible && onStepChange(step.id)}
                  disabled={!isAccessible}
                  className={cn(
                    "flex-1 py-2 text-center text-xs transition-all border-b-2",
                    isActive && "border-primary text-primary",
                    isCompleted && "border-primary/40 text-primary/60",
                    !isActive && !isCompleted && "border-transparent text-muted-foreground"
                  )}
                >
                  {step.label}
                </button>
              );
            })}
          </div>
        </div>
      </header>

      {/* Main */}
      <main className="flex-1">
        <div className="mx-auto max-w-7xl px-4 py-6 sm:px-6 sm:py-8 lg:px-8">
          {children}
        </div>
      </main>
    </div>
  );
}
