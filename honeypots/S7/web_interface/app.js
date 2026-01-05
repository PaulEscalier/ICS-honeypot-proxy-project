const ws = new WebSocket(`ws://${location.host}/ws`);
const alerts = document.getElementById("alerts");

ws.onmessage = (event) => {
  const d = JSON.parse(event.data);

  set("speed", d.motor_speed.toFixed(1));
  set("load", d.load_weight.toFixed(1));
  set("temp", d.temperature.toFixed(1));

  setState("belt", d.belt_running);
  setState("jam", d.jam_detected);
  setState("estop", d.emergency_stop);
};

function set(id, val) {
  document.getElementById(id).textContent = val;
}

function setState(id, state) {
  const el = document.getElementById(id);
  el.textContent = state ? "ON" : "OFF";
  el.className = state ? "alarm" : "ok";
}
