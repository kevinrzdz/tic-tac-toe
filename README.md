# Tic-Tac-Toe AI with Minimax Algorithm

A web-based tic-tac-toe game featuring an unbeatable AI opponent powered by the minimax algorithm.

## Features

- **Unbeatable AI**: Implements the minimax algorithm for optimal gameplay
- **Player Choice**: Choose to play as X (first) or O (second)
- **Real-time Gameplay**: Instant moves and game state updates
- **Responsive Design**: Works seamlessly on desktop and mobile devices
- **Clean Interface**: Modern, gradient-styled UI with smooth animations
- **Session Management**: Maintains game state throughout your session

## How It Works

The AI uses the **minimax algorithm**, a decision-making algorithm that:

- Explores all possible game outcomes
- Assumes both players play optimally
- Chooses moves that maximize the AI's chances while minimizing yours
- Guarantees the AI will never lose (it will either win or tie)

## Installation

1. Clone this repository

```bash
git clone https://github.com/kevinrzdz/tic-tac-toe.git
```

2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

3. Run the application:

```bash
python app.py
```

4. Open your browser and navigate to `http://localhost:5000`

## Project Structure

```
├── app.py              # Flask web application
├── tictactoe.py        # Core game logic and minimax algorithm
├── requirements.txt    # Python dependencies
├── templates/
│   └── index.html     # Main game interface
└── static/
    └── style.css      # Styling and responsive design
```

## Technical Details

### Backend (Flask)

- RESTful API endpoints for game management
- Session-based game state tracking
- JSON responses for real-time updates

### Game Logic

- **Minimax Algorithm**: Recursive decision tree exploration
- **Alpha-Beta Optimization**: Early termination for efficiency
- **Move Validation**: Comprehensive input checking
- **Win Detection**: All possible winning combinations

### Frontend

- **Responsive Grid**: CSS Grid-based game board
- **Interactive UI**: Hover effects and smooth transitions
- **Real-time Updates**: AJAX-based move handling
- **Mobile Friendly**: Optimized for touch devices

## API Endpoints

- `POST /new_game` - Start a new game with player selection
- `POST /make_move` - Submit a player move and get AI response
- `GET /game_state` - Retrieve current game status

## Dependencies

- **Flask 3.1.1**: Web framework for the backend server
