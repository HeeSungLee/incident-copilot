#Un incidente válido mínimo pasa, y los valores por defecto son correctos (status == open, timestamps con zona horaria).
#Una severidad inválida falla.
#Un título vacío, solo con espacios o de más de 200 caracteres falla. Usa @pytest.mark.parametrize.
#Un campo extra falla.
#Un updated_at anterior a created_at falla.
#Round-trip: convertir a JSON y volver da el mismo objeto.

   #uv run pytest -v && uv run ruff check . && uv run ruff format --check .