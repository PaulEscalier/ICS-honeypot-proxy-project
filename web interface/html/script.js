async function sendInterrogation() {
  await fetch("/interrogation", { method: "POST" });
}

async function sendCmd(state) {
  const ioa = document.getElementById("ioa").value;

  await fetch("/send", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ ioa, state }),
  });

  console.log("Send: " + state);
}

async function sendOpcUaInterrogation() {
  await fetch("/opcUaActivity", { method: "GET" });
}
async function sendModbusInterrogation() {
  await fetch("/modbusActivity", { method: "GET" });
}

async function sendOpcUaInterrogation() {
  await fetch("/opcUaActivity", { method: "GET" });
}

async function sendS7Interrogation() {
  await fetch("/s7Activity", { method: "GET" });
}
