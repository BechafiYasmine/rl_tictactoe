from game import TicTacToeGame
from agent import QLearningAgent
from gui import TicTacToeGUI

def train_agent(episodes=5000):
    """Train the agent"""
    print(f"Training AI for {episodes} games...")
    
    game = TicTacToeGame()
    agent = QLearningAgent(player='X')
    
    for episode in range(episodes):
        state = game.reset()
        done = False
        
        while not done:
            valid_moves = game.get_valid_moves()
            move = agent.choose_move(game.board, valid_moves)
            new_state, reward, done, winner = game.make_move(move)
            
            if done and winner == 'X':
                agent_reward = 1
            elif done and winner == 'O':
                agent_reward = -1
            elif done:
                agent_reward = 0
            else:
                agent_reward = -0.01
            
            agent.learn(state, move, agent_reward, new_state, done)
            state = new_state
        
        agent.become_less_curious()
        
        if (episode + 1) % 100 == 0:
            print(f"Episode {episode + 1}/{episodes}")
    
    print("Training complete!")
    return agent

def main():
    print("="*50)
    print("TIC-TAC-TOE REINFORCEMENT LEARNING")
    print("="*50)
    
    print("\nTraining AI (500 games)...")
    agent = train_agent(500)
    
    print("\nLaunching game window...")
    gui = TicTacToeGUI(agent)
    gui.run()

if __name__ == "__main__":
    main()