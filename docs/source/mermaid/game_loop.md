flowchart TD;

Start --> Loop[Main Loop]

Loop --> Input[Read input state]

Input --> UP[Update Physics with Input]
UP --> T[Tick Physics]
T --> PS[Get Physics State]

PS --> HA[Handle Input Audio]
HA --> R[Render View]

R --> GO{Game over?}
GO --> |No| Loop
GO --> |Yes| End