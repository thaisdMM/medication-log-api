import capsule from "./assets/capsule.svg";

function App() {
  return (
    <main className="flex min-h-svh flex-col items-center justify-center gap-6 bg-slate-50 p-8 text-center">
      <img src={capsule} alt="A medication capsule" className="size-32" />
      <h1 className="text-5xl font-bold text-blue-800">Medication Log</h1>
      <p className="max-w-xl text-2xl text-slate-800">
        Test page: if this text is large and dark on a light background, the
        styles loaded.
      </p>
    </main>
  );
}

export default App;
