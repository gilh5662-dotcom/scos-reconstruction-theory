# SCOS Architecture

## Encoding

```text
   +-----------------------+
   | Large Data File       |  (example: text, image, or bitstream)
   +-----------+-----------+
               |
               v  [Modulated Trigger Function]
   +-----------------------+
   | Compact Digital Seed  |
   +-----------+-----------+
               |
               v  [Open-System Interaction]
   +-----------------------+
   | Physical State Medium |  (example: optical, analog, material, or reservoir state)
   +-----------+-----------+
               |
               v
   +-----------------------+
   | Captured Medium State |
   +-----------------------+
```

## Reconstruction

```text
   +-----------------------+
   | Digital Seed          |
   +-----------+-----------+
               |
               v  [Interaction / Reconstruction Operator]
   +-----------------------+
   | Preserved Medium State|  (requires state fidelity)
   +-----------+-----------+
               |
               v  [Deterministic State Evaluation]
   +-----------------------+
   | Reconstructed Data    |
   +-----------------------+
```

## System Requirement

The digital seed is not sufficient by itself. Reconstruction depends on the
seed, the interaction dynamics, and the associated physical state or an
equivalent representation of that state.
