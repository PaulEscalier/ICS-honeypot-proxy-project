const ws = new WebSocket(`ws://${location.host}/ws`);

ws.onmessage = (event) => {
  const d = JSON.parse(event.data);

  setStatus("b1", d.breaker_1);
  setStatus("b2", d.breaker_2);

  document.getElementById("u").textContent = d.voltage_kv.toFixed(1);
  document.getElementById("i").textContent = d.current_a.toFixed(1);
  document.getElementById("f").textContent = d.frequency_hz.toFixed(2);
};

function setStatus(id, state) {
  const el = document.getElementById(id);
  el.textContent = state ? "CLOSED" : "OPEN";
  el.className = state ? "on" : "off";
}
