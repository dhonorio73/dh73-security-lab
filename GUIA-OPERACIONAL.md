# Guia operacional — Dh73 Security Lab

Este guia define os limites do protótipo, o fluxo de autorização e os controles mínimos antes de qualquer piloto. O simulador atual processa somente cabeçalhos fornecidos pelo operador. **Ele não consulta domínios, não envia requisições e não é um serviço de auditoria.**

## 1. Escopo do produto atual

### Dentro do escopo

- Importar um arquivo JSON local de até 1 MiB ou colar os dados no navegador.
- Analisar os seis cabeçalhos de segurança documentados no README.
- Mostrar verificações heurísticas e recomendações educativas.
- Registrar no relatório os campos de escopo e a referência de autorização informados pelo operador.
- Gerar uma impressão/PDF iniciado pelo usuário.

### Fora do escopo

- Consultar URL, DNS, HTTP ou HTTPS; fazer varredura, enumeração ou descoberta de ativos.
- Executar exploits, testes de intrusão, autenticação ou alterações no sistema do cliente.
- Validar que a autorização informada é verdadeira ou que o material pertence ao ativo declarado.
- Emitir certificação, pontuação de conformidade ou garantia de segurança.
- Armazenar, transmitir, compartilhar ou reter automaticamente os dados do cliente.

Qualquer ampliação para coleta técnica em ativos reais exige nova avaliação de segurança, privacidade, autorização, escopo, infraestrutura e revisão jurídica. Não habilitar descoberta ou análise de domínios arbitrários.

## 2. Procedimento de autorização e escopo

Antes de receber dados de um cliente, o responsável pela avaliação deve confirmar e manter, fora desta ferramenta, evidência escrita com:

1. Entidade proprietária e responsável que autorizou a análise.
2. Operador autorizado e canal de contato.
3. Identificador exato do ativo/aplicação e ambiente coberto.
4. Finalidade, dados permitidos e período de validade.
5. Exclusões, restrições de compartilhamento e procedimento de interrupção.
6. Referência rastreável a contrato, chamado ou autorização assinada.

O operador informa no relatório o ativo e a referência e confirma uma declaração de autorização vigente. Esses campos são **autodeclarados**; a aplicação não verifica documentos, identidade, propriedade ou escopo. A confirmação na interface não substitui contrato, consentimento nem revisão jurídica.

Não inserir URLs como pedido de consulta, credenciais, cookies, tokens, dados pessoais ou conteúdo de resposta que não seja necessário. Remover `Set-Cookie`, `Authorization`, identificadores e valores sensíveis antes de importar os cabeçalhos.

### Registro operacional de autorização

Use este checklist para conferir a evidência mantida no processo do cliente. É um registro operacional, **não um contrato ou aconselhamento jurídico**:

```text
Cliente / proprietário do ativo:
Responsável que autorizou e função:
Operador autorizado:
Ativo e ambiente exatamente cobertos:
Finalidade e dados permitidos:
Início e término da autorização:
Exclusões e restrições:
Contato para interromper o trabalho:
Referência do documento/chamado aprovado:
Responsável interno que conferiu a evidência:
```

Não anexar o documento de autorização ao simulador. A interface registra apenas a referência que o operador informar.

## 3. Validação da análise

As regras atuais são heurísticas educativas implementadas no simulador:

| Cabeçalho | Verificações básicas | Limitação que exige revisão humana |
|---|---|---|
| `Content-Security-Policy` | Procura `default-src`, curinga e `unsafe-inline`/`unsafe-eval`. | Não analisa a gramática completa, fontes por diretiva, nonces, hashes, caminhos ou compatibilidade da aplicação. Sempre revisar manualmente. |
| `Strict-Transport-Security` | Procura `max-age` numérico de pelo menos 31.536.000 segundos. | Não verifica HTTPS no ativo, subdomínios, preload ou adequação operacional. |
| `X-Content-Type-Options` | Espera o valor `nosniff`. | Não valida MIME types nem o comportamento do servidor. |
| `X-Frame-Options` | Reconhece `DENY` e `SAMEORIGIN`. | Não avalia necessidades de integração; preferências de framing modernas também podem usar CSP `frame-ancestors`. |
| `Referrer-Policy` | Reconhece políticas conhecidas e sinaliza opções mais permissivas. | Não determina se a política atende ao fluxo, produto ou requisitos de privacidade. |
| `Permissions-Policy` | Verifica uma forma sintática simplificada de diretivas. | Não confere nomes válidos de funcionalidades, suporte do navegador nem necessidade de cada origem. |

### Critérios mínimos para validar uma versão

- Executar a suíte automatizada do verificador Python.
- Verificar no navegador os cenários demonstrativos, valores incorretos, JSON inválido, campos de autorização incompletos e alteração de dados após análise.
- Testar importação de JSON válido, arquivo acima de 1 MiB, formato não JSON e erro de leitura.
- Confirmar que conteúdo importado aparece apenas como texto e não é interpretado como HTML.
- Confirmar que não existem requisições de rede, armazenamento persistente, telemetria ou envio de dados.
- Manter exemplos conhecidos e revisar as regras com profissional qualificado antes de usar em avaliação contratada.

Resultado de regra automatizada não deve ser comunicado como “site seguro”. Usar “adequado na verificação básica”, “revisão manual”, “ausente” ou “formato básico válido”, sempre com as limitações junto do resultado.

## 4. Segurança e privacidade

- A análise ocorre no navegador. Não há backend, analytics, armazenamento local implementado ou envio de dados pela aplicação.
- O arquivo selecionado é lido pelo navegador localmente; o limite do simulador é 1 MiB.
- O relatório pode conter identificadores e dados do cliente. O usuário controla impressão e salvamento; seguir a política contratual do cliente para compartilhar e excluir o PDF.
- Usar dados mínimos e sanitizados. Não importar cabeçalhos de autenticação, cookies ou dados pessoais.
- Valores dinâmicos devem continuar sendo inseridos como texto (`textContent`), nunca concatenados como HTML.
- Não adicionar bibliotecas, fontes remotas, analytics, APIs ou chamadas `fetch` sem nova revisão de privacidade e segurança.
- Antes da distribuição, verificar código-fonte, dependências, políticas de conteúdo, hospedagem, controle de acesso e comportamento de rede da versão publicada.

## 5. Implantação e publicação

### Uso local/piloto controlado

Distribuir o código e instruções de integridade do pacote por canal acordado. O cliente abre o HTML localmente e fornece um JSON sanitizado. Registrar versão da ferramenta e versão do guia no relatório ou no registro de trabalho.

### Hospedagem estática

Publicar somente após revisão e aprovação do responsável pelo produto. Usar domínio controlado, HTTPS, acesso e processo de atualização adequados ao público. A página hospedada baixa o código para o navegador do usuário; confirmar por inspeção independente que os dados analisados não são transmitidos ao servidor de hospedagem. A política CSP deve ser compatível com os scripts do produto; preferir scripts externos com hashes/nonce em vez de liberar scripts inline indiscriminadamente.

Cada versão deve ter changelog, revisão, teste, responsável, plano de rollback e canal para comunicação de incidentes. Não anunciar como scanner, auditoria automatizada ou certificação.

## 6. Suporte e incidentes

- Registrar versão, navegador, passos para reproduzir e JSON de teste sanitizado; nunca pedir credenciais ou cabeçalhos sensíveis.
- Separar defeitos de interface, erro de regra, solicitação de privacidade e vulnerabilidade de segurança.
- Interromper o uso e retirar a versão afetada se houver envio inesperado de dados, execução de conteúdo importado ou resultado enganoso.
- Definir antes do piloto: canal de suporte, responsável, horários, prazo de resposta, política de retenção e procedimento de notificação. Nenhum SLA está prometido por este protótipo.
- Encaminhar dúvidas legais, privacidade, contratos e comercialização a profissionais qualificados na jurisdição e no mercado atendidos.

## 7. Prontidão comercial

Este protótipo **não está pronto para comercialização**. Antes de cobrar por avaliações, são necessários, no mínimo: revisão independente das regras, política de privacidade e termos, contrato e autorização aprovados, avaliação de risco, estratégia de hospedagem e dados, testes de segurança/acessibilidade, suporte definido e validação com clientes-piloto sob escopo escrito.

## 8. Resultado da verificação do protótipo

Verificações realizadas em 31/10/2026, no protótipo local:

| Verificação | Resultado | Evidência / limite |
|---|---|---|
| Testes Python existentes | Aprovado: 8/8 | Execução da suíte `unittest`; cobre o analisador offline e o relatório Python. |
| Cenário com lacunas e cenário completo | Aprovado | Interface mostrou, respectivamente, 2 adequados + 4 ausentes e 5 adequados + 1 revisão manual. |
| Cenário com valores problemáticos | Aprovado | Os seis cabeçalhos foram marcados para revisão. |
| Bloqueio até informar ativo, referência e consentimento | Aprovado | Botão de análise permanece desabilitado até preencher os campos e marcar a confirmação. |
| Reautorização após edição/importação | Aprovado | A edição dos dados e a escolha de outro arquivo limpam o resultado e exigem nova confirmação. |
| JSON inválido | Aprovado | O resumo é invalidado, contadores são limpos e os itens anteriores desaparecem. |
| Importação de arquivo local | Aprovado | Arquivo de exemplo lido localmente; interface exige autorização antes da análise. |
| Limite de arquivo acima de 1 MiB | Aprovado | Arquivo de teste de 1.048.577 bytes foi recusado com mensagem explícita. |
| Conteúdo semelhante a HTML/script nos campos | Aprovado no teste manual | Texto foi exibido como texto; nenhum elemento injetado foi criado. |
| Requisições de rede durante interação | Nenhuma observada | Instrumentação do navegador registrou zero requisições nos cenários; inspeção do HTML não encontrou APIs de rede, armazenamento ou scripts externos. Não é uma auditoria independente do navegador ou do ambiente de hospedagem. |
| Layout responsivo e impressão | Aprovado em verificação manual | Sem overflow horizontal no viewport estreito testado; impressão oculta entrada e mantém o relatório. |

### Bloqueios para venda/produção

- **Análise técnica:** regras ainda são heurísticas; falta revisão independente e uma suíte de casos de referência aprovada por profissional qualificado.
- **Autorização:** a confirmação é autodeclarada e não autentica o operador, verifica documentos ou valida titularidade do ativo.
- **Jurídico e privacidade:** termos, contrato, política de privacidade, retenção e responsabilidades ainda não foram revisados por profissionais na jurisdição de operação.
- **Implantação:** não há release assinado, processo de publicação/rollback, configuração CSP final nem revisão independente da hospedagem.
- **Operação comercial:** suporte, responsável, canal de incidente, SLA, processo de piloto e condições comerciais ainda precisam ser definidos.

**Decisão desta revisão: apto para demonstração e piloto local controlado com dados sanitizados; não aprovado para venda como auditoria, serviço de varredura ou produto de segurança em produção.** Esta avaliação é técnica e operacional, não constitui validação jurídica, certificação ou garantia de segurança.
