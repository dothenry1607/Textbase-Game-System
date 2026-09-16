const status = document.querySelector("#status");
const message = document.querySelector("#message");
async function call(url, options = {}) {
  const response = await fetch(url, { headers: {"Content-Type": "application/json"}, ...options });
  const data = await response.json();
  if (!response.ok) throw new Error(data.detail || "Request failed");
  return data;
}
function show(data) {
  status.textContent = JSON.stringify(data, null, 2);
  if (data.message) message.textContent = data.message;
}
async function refresh() { try { show(await call("/api/status")); } catch (e) { message.textContent = e.message; } }
document.querySelector("#setup").addEventListener("submit", async (event) => {
  event.preventDefault();
  const form = new FormData(event.currentTarget);
  try { show(await call("/api/setup", {method: "POST", body: JSON.stringify(Object.fromEntries(form))})); }
  catch (e) { message.textContent = e.message; }
});
document.querySelectorAll("[data-action]").forEach((button) => button.addEventListener("click", async () => {
  try { show(await call("/api/action", {method: "POST", body: JSON.stringify({action: button.dataset.action, item: button.dataset.item})})); }
  catch (e) { message.textContent = e.message; }
}));
refresh();
