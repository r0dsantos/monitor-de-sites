# Monitor de Sites

Script em Python que verifica se uma lista de sites esta no ar, mede o tempo de
resposta e salva um relatorio em CSV. O projeto roda em container Docker e tem
pipeline de CI no GitHub Actions.

## O que ele faz
- Le os sites de `sites.txt`
- Faz uma requisicao HTTP em cada um
- Mostra no terminal: no ar ou fora, status e tempo (ms)
- Salva o historico em `relatorio.csv`
- Termina com codigo de erro (1) se algum site estiver fora, para uso em automacao

## Tecnologias
Python 3 (biblioteca padrao), Docker, Git/GitHub, GitHub Actions

## Como rodar

**Direto no Python:**
```bash
python monitor.py
```

**Com Docker:**
```bash
docker build -t monitor-de-sites .
docker run --rm monitor-de-sites
```

**Testes:**
```bash
python -m unittest -v
```

## Pipeline (CI)
A cada push, o GitHub Actions roda os testes e constroi a imagem Docker
(`.github/workflows/ci.yml`).

## Proximos passos (ideias de evolucao)
- [ ] Enviar alerta por e-mail ou Telegram quando um site cair
- [ ] Agendar a execucao a cada 5 minutos (cron)
- [ ] Gerar grafico de disponibilidade a partir do CSV
- [ ] Publicar a imagem no Docker Hub pelo pipeline
