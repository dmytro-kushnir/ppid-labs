# UART transmitter and receiver algorithms (довідково)

Reference flowcharts for understanding Lab 1 — **not required in the student report**. Reports use Wokwi screenshots + host logs (`Verify: OK`), not hand-drawn diagrams.

## Transmitter

```mermaid
flowchart TD
  start([Start]) --> open[open_port]
  open --> cfg[configure_port baud 8N1]
  cfg --> send[send_message text plus CR]
  send --> close[close_port]
  close --> endNode([End])
```

## Receiver

```mermaid
flowchart TD
  start([Start]) --> open[open_port]
  open --> cfg[configure_port same as TX]
  cfg --> loop{bytes available?}
  loop -->|yes| read[read_until CR]
  read --> decode[decode ASCII]
  decode --> show[print message]
  show --> loop
  loop -->|timeout| close[close_port]
  close --> endNode([End])
```

Code: [host/uart_host.py](../../host/uart_host.py), Wokwi: [wokwi/lab01-uart/](../../wokwi/lab01-uart/).
