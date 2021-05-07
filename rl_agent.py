from collections import deque

class ReplayExperience:
  def __init__(self, size):
    self.memory = deque(maxlen=size)

  def add(self, batch):
    self.memory.append(batch)

  def sample(self, size):
    return random.sample(self.memory, size)

  def __len__(self):
    return len(self.memory)

class DQN:
    def __init__(self, state_space, action_space, learning_rate=0.001, hidden_dimensions=16, memory_size=10000, batch_size=64, gamma=0.99, eps=1, eps_decay=0.99, eps_min=0.001):
    self.replay_experience = ReplayExperience(memory_size)

    self.batch_size=batch_size
    self.gamma = gamma
    self.eps = eps
    self.eps_min = eps_min
    self.eps_decay = eps_decay

    self.state_space = state_space
    self.action_space = action_space
    
    self.local = torch.nn.Sequential(
            torch.nn.Linear(self.state_space, hidden_dimensions),
            torch.nn.ReLU(),
            torch.nn.Linear(hidden_dimensions, hidden_dimensions),
            torch.nn.ReLU(),
            # torch.nn.Linear(hidden_dimensions, hidden_dimensions),
            # torch.nn.ReLU(),
            torch.nn.Linear(hidden_dimensions, self.action_space)
        )

    self.target = torch.nn.Sequential(
            torch.nn.Linear(self.state_space, hidden_dimensions),
            torch.nn.ReLU(),
            torch.nn.Linear(hidden_dimensions, hidden_dimensions),
            torch.nn.ReLU(),
            # torch.nn.Linear(hidden_dimensions, hidden_dimensions),
            # torch.nn.ReLU(),
            torch.nn.Linear(hidden_dimensions, self.action_space)
        )

    self.criterion = torch.nn.MSELoss()
    # TODO: check these two lines # NOTE: done need target_optimizer
    self.local_optimizer = torch.optim.Adam(self.local.parameters(), learning_rate)
    # self.target_optimizer = torch.optim.Adam(self.target.parameters(), learning_rate)

  # local model only
  def predict(self, state):
        with torch.no_grad():
            return self.local(torch.Tensor(state))

  # get action from local network
  def action(self, state):
    if np.random.random() <= self.eps:
      return random.randrange(self.action_space)
    q_values = self.predict(state)
    return torch.argmax(q_values).item()

  # TODO: fix this function
  def update(self, states, targets):
        loss = self.criterion(self.local(torch.Tensor(states)), Variable(torch.Tensor(targets)))
        self.local_optimizer.zero_grad()
        loss.backward()
        self.local_optimizer.step()

  def replay(self):
    if len(self.replay_experience) < self.batch_size:
            return
    batch = self.replay_experience.sample(self.batch_size)
    states, next_states = np.zeros((self.batch_size, self.state_space)), np.zeros((self.batch_size, self.state_space))
    actions, rewards, dones = [], [], []

    for i in range(len(batch)):
      states[i] = batch[i][0]
      actions.append(batch[i][1])
      rewards.append(batch[i][2])
      next_states[i] = batch[i][3]
      dones.append(batch[i][4])

    targets = self.local(torch.Tensor(states))
    next_targets = self.local(torch.Tensor(next_states)).detach().numpy()
    next_targets_from_target = self.target(torch.Tensor(next_states)).detach().numpy()

    for i in range(len(batch)):
      action = np.argmax(next_targets[i])
      targets[i][actions[i]] = rewards[i] + (1-dones[i])*self.gamma*next_targets_from_target[i][action]

    self.update(states, targets)
    self.eps *= self.eps_decay
    self.eps = max(self.eps, self.eps_min)

  # this only operates on the target network
  def update_target(self):
    self.target.load_state_dict(self.local.state_dict())

# def train(max_episodes, env, agent, i=0):

#   total_scores = []

#   scores = deque(maxlen=100)

#   for episode in range(max_episodes):
#     state, done = env.reset(), False
#     step = 0

#     while not done:
#       action = agent.action(state)
#       next_state, reward, done, _ = env.step(action)
#       step += 1

#       agent.replay_experience.add((state, action, reward, next_state, done))
#       state = next_state

#       if done:
#         agent.update_target()
#         scores.append(step)
#         print("{}, {}, {}, {}, {}, {}".format(i, episode, agent.eps, np.mean(scores), 0, step))
#         break

#       if step < 475:
#         agent.replay()
#     if np.mean(scores) >= env.spec.reward_threshold:
#       break