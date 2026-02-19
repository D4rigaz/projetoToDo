# 📝 Check-It: Histórico de Desenvolvimento

Este documento registra a evolução, os desafios técnicos e as soluções aplicadas no desenvolvimento do aplicativo **Check-It To-Do App**.

## 🚀 Versão Atual: Modern Flat (v2.0)
- **Design:** Modern Dark Neon (GitHub Space theme).
- **Estabilidade:** Hierarquia de renderização zero (achatada) para compatibilidade 100% com Flet Web.
- **Persistência:** Arquivo JSON local (`todo_data.json`).
- **Validação:** Pipeline de QA com evidências visuais em JPG.

---

## 📅 Jornada de Desenvolvimento

### 🟢 Fase 1: Fundação (v1.0)
- **Objetivo:** Criar um app Windows funcional em Python.
- **Tecnologia:** Flet (baseado em Flutter).
- **Desafios:** Configuração inicial de ambiente e lógica de salvar tarefas.
- **Resultado:** App funcional em Dark Mode com filtros de tarefas.

### 🟠 Fase 2: Modernização e Web (v1.5)
- **Objetivo:** Mover o app para o navegador e melhorar a estética.
- **Decisão Técnica:** Migração para `view=ft.AppView.WEB_BROWSER`.
- **Bug Crítico:** "O Quadrado Cinza" (Erro de renderização do Flutter Web em containers aninhados).
- **Solução:** Revisor e QA implementaram a **Hierarquia Zero**, removendo containers agrupadores e adicionando componentes diretamente na página.

### 🔵 Fase 3: Profissionalização (Pipeline de QA)
- **Equipe:** Adição dos perfis de **UI/UX**, **REVISOR** e **QA**.
- **Novo Fluxo:** Cada alteração agora passa por revisão de código e teste de QA.
- **Evidências:** Implementação de um gerador de relatórios em `.jpg` usando a biblioteca Pillow para comprovação de sucesso visual.

---

## 🛠️ Decisões da Equipe Técnica

### 🎨 UI/UX (Design)
- Uso da cor `#5865F2` (Indigo) para identidade de marca.
- Fundo `#0D1117` para reduzir o cansaço visual.
- Botões com bordas arredondadas de 10px para um visual moderno.

### 🔍 REVISOR (Código)
- **Veto de Containers:** Proibido o uso de `ft.Container` como pai de layout para evitar o colapso gráfico no navegador.
- **Strings Diretas:** Uso de strings literais para cores e ícones para evitar erros de atributo em diferentes versões do Flet.

### 🛡️ QA (Qualidade)
- **Botões Estáveis:** Uso de `ElevatedButton` em vez de botões customizados para garantir interatividade em qualquer browser.
- **Evidências:** Pasta `evidencias/` contendo arquivos JPG com carimbo de tempo e status do teste.

---

## 📋 Próximos Passos (Backlog)
- [ ] Adicionar categorias coloridas para tarefas.
- [ ] Implementar datas de entrega (Deadlines).
- [ ] Criar sistema de notificações no navegador.
- [ ] Deploy em servidor remoto (Replit/Vercel).

---
*Gerado por Gemini CLI em colaboração com a equipe de UI/UX, Revisor e QA.*
