const form = document.querySelector('#form');
const result = document.querySelector('#result');
form.addEventListener('submit', async (event) => {
  event.preventDefault();
  const payload = Object.fromEntries(new FormData(form).entries());
  for (const key of Object.keys(payload)) payload[key] = Number(payload[key]);
  result.textContent = 'Calculando...';
  try {
    const response = await fetch('/api/predict', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) });
    const data = await response.json();
    if (!response.ok) throw new Error(`Error ${response.status}: revisa los valores ingresados`);
    result.textContent = `Especie: Iris ${data.species} · Confianza: ${(data.confidence * 100).toFixed(1)}%`;
  } catch (error) { result.textContent = `No fue posible predecir. ${error.message}`; }
});
