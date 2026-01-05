const ws = new WebSocket(`ws://${location.host}/ws`);

ws.onmessage = (event) => {
  const d = JSON.parse(event.data);

  document.getElementById("temp").textContent = d.temperature.toFixed(1);
  document.getElementById("power").textContent = d.heater_power.toFixed(0);
  document.getElementById("mass").textContent = d.load_mass.toFixed(0);

  setBool("cooling", d.cooling, "ON", "OFF");
  setBool("alarm", d.alarm, "ACTIVE", "NORMAL");
};

function setBool(id, value, onText, offText) {
  const el = document.getElementById(id);
  el.textContent = value ? onText : offText;
  el.className = value ? "on" : "off";
}
