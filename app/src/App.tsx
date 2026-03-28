import { useState } from "react";
import { Layout } from "@/components/Layout";
import { IntakePage } from "@/pages/IntakePage";
import { HiringPackPage } from "@/pages/HiringPackPage";
import { CandidateScreenPage } from "@/pages/CandidateScreenPage";

function App() {
  const [currentStep, setCurrentStep] = useState(1);
  const [maxStep, setMaxStep] = useState(1);

  const goToStep = (step: number) => {
    setCurrentStep(step);
    setMaxStep((prev) => Math.max(prev, step));
  };

  return (
    <Layout
      currentStep={currentStep}
      onStepChange={setCurrentStep}
      maxStep={maxStep}
    >
      {currentStep === 1 && (
        <IntakePage onAnalysisComplete={() => goToStep(2)} />
      )}
      {currentStep === 2 && (
        <HiringPackPage onNext={() => goToStep(3)} />
      )}
      {currentStep === 3 && <CandidateScreenPage />}
    </Layout>
  );
}

export default App;
