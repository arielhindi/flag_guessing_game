# Copilot Instructions for flag_guessing_game

## Project Overview

**flag_guessing_game** is an interactive game where users guess country flags. The project is organized by daily challenges (day01, day02, etc.), with each day containing game logic, UI components, and fetching mechanisms.

## Project Structure

```
flag_guessing_game/
├── README.md
├── .github/
│   └── copilot-instructions.md (this file)
├── game/
│   ├── day06/
│   │   ├── game_logic.py        # Core game state and round logic
│   │   ├── fetcher.py           # Data fetching for flags
│   │   ├── ui.py                # User interface components
│   │   └── ...
│   ├── day07/
│   └── ...
```

## Key Concepts & Architecture

### GameState Class (`game_logic.py`)
- Tracks: `total_rounds`, `correct`, and `current` round data
- Methods:
  - `next_round()`: Generates next round with flag and multiple choice options
  - `submit_guess()`: Validates guesses and updates score
  - Note: `total_rounds` is only incremented when a guess is submitted, not when a round is generated

### Data Flow
1. **Fetcher** retrieves flag data (country names, flag URLs, etc.)
2. **GameState** manages game logic and tracks progress
3. **UI** displays flags and accepts user input
4. Guesses are validated and score is updated

## Code Style Guidelines

### Python
- Follow **PEP 8** style guidelines
- Use **type hints** for all function parameters and return types
- Use **dataclasses** for data structures when appropriate
- Include **docstrings** for all classes and public methods
- Use **relative imports** within day directories (e.g., `from . import fetcher`)
- Include fallback imports for flexibility (try/except patterns)

### Comments & Documentation
- Document non-obvious logic clearly
- Use docstrings (Google style or NumPy style)
- Keep comments concise and focused

## Common Tasks

### Adding a New Round Feature
1. Modify `GameState` to track new attributes
2. Update `next_round()` to include new data
3. Update `submit_guess()` validation logic
4. Update UI components to display new information

### Adding a New Day Challenge
1. Create `game/dayXX/` directory
2. Implement `game_logic.py` with `GameState` class
3. Implement `fetcher.py` for data retrieval
4. Implement `ui.py` for user interface
5. Follow existing patterns from previous days

### Debugging
- Use print statements or logging for debugging
- Check that `total_rounds` increment logic is correct
- Validate that correct/incorrect guess counts are accurate

## Testing Considerations

- Test edge cases (no data available, invalid inputs)
- Verify score calculation accuracy
- Ensure UI displays all choices correctly
- Test round generation randomization

## Dependencies & Imports

- Core: `dataclasses`, `typing`, `random`
- Data handling: Varies by day (flags, country data, etc.)
- UI: Depends on implementation (terminal, web, etc.)

## Best Practices

1. **Modularity**: Keep game logic, data fetching, and UI separate
2. **Immutability**: Avoid modifying game state unexpectedly
3. **Randomization**: Use `random` module for variety in question selection
4. **Error Handling**: Handle missing or invalid data gracefully
5. **Reusability**: Extract common patterns into utility functions

## Notes

- Each day can have its own variations on the core game mechanics
- The project uses optional relative imports for flexibility
- When suggesting code, maintain consistency with existing patterns
- Always validate user input before updating game state
