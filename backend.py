from flask import Flask, request, jsonify, render_template, send_file
import networkx as nx
from collections import deque
import heapq
import os
import json
import base64

app = Flask(__name__)

class MazeGraph:
    def __init__(self):
        # Create a graph representation for the maze
        self.graph = {}
        self.heuristic = {}
        
    def add_edge(self, u, v, weight=1):
        if u not in self.graph:
            self.graph[u] = []
        if v not in self.graph:
            self.graph[v] = []
        
        self.graph[u].append((v, weight))
        self.graph[v].append((u, weight))
    
    def set_heuristic(self, state, value):
        self.heuristic[state] = value
        
    def get_neighbors(self, node):
        return self.graph.get(node, [])
    
    def breadth_first_search(self, start, goal):
        if start == goal:
            return [start], [start]
            
        # Initialize visited set, queue, and parent dictionary
        visited = set([start])
        queue = deque([start])
        parent = {start: None}
        explored_path = [start]
        
        while queue:
            node = queue.popleft()
            
            for neighbor, _ in self.get_neighbors(node):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
                    parent[neighbor] = node
                    explored_path.append(neighbor)
                    
                    if neighbor == goal:
                        # Reconstruct solution path from parent dictionary
                        solution_path = []
                        current = neighbor
                        while current is not None:
                            solution_path.append(current)
                            current = parent[current]
                        solution_path.reverse()
                        return explored_path, solution_path
        
        return explored_path, []
    
    def depth_first_search(self, start, goal):
        """Implement DFS algorithm"""
        if start == goal:
            return [start], [start]
        
        visited = set()
        stack = [(start, None)]  # (node, parent)
        parent = {}
        explored_path = []
        
        while stack:
            node, node_parent = stack.pop()
            
            if node not in visited:
                visited.add(node)
                explored_path.append(node)
                parent[node] = node_parent
                
                if node == goal:
                    solution_path = []
                    current = node
                    while current is not None:
                        solution_path.append(current)
                        current = parent[current]
                    solution_path.reverse()
                    return explored_path, solution_path
                
                neighbors = self.get_neighbors(node)
                for neighbor, _ in reversed(neighbors):
                    if neighbor not in visited:
                        stack.append((neighbor, node))
        
        return explored_path, []
    
    def a_star_search(self, start, goal):
        """Implement A* algorithm"""
        if start == goal:
            return [start], [start]
        
        open_set = [(self.heuristic[start], 0, start, None)]  # (f, g, node, parent)
        heapq.heapify(open_set)
        closed_set = set()
        g_values = {start: 0}
        parent = {}
        explored_path = []
        
        while open_set:
            f, g, node, node_parent = heapq.heappop(open_set)
            
            if node in closed_set:
                continue
                
            explored_path.append(node)
            parent[node] = node_parent
            closed_set.add(node)
            
            if node == goal:
                solution_path = []
                current = node
                while current is not None:
                    solution_path.append(current)
                    current = parent[current]
                solution_path.reverse()
                return explored_path, solution_path
            
            for neighbor, weight in self.get_neighbors(node):
                if neighbor in closed_set:
                    continue
                    
                tentative_g = g + weight
                
                if neighbor not in g_values or tentative_g < g_values[neighbor]:
                    g_values[neighbor] = tentative_g
                    f = tentative_g + self.heuristic.get(neighbor, 0)
                    heapq.heappush(open_set, (f, tentative_g, neighbor, node))
        
        return explored_path, []

def create_maze():
    maze = MazeGraph()
   
    edges = [
        # Row 1 connections
        ('A', '1'),
        ('1', '2'),
        ('2', '3'), ('2', '4'),
        ('4', '10'),
        # Row 2 connections
        ('3', '5'), 
        ('5', '6'), ('5', '7'),
        ('7', '9'),
        # Row 3 connections
        ('6', '8'), 
        ('10', '11'), ('10', '12'),
        ('12', '13'),
        ('13', '14'),
        ('14', '17'),
        ('14', '15'),
        # Row 4 connections
        ('15', '16'),
        ('17', '18'), ('17', '20'),
        ('18', '19'),
        ('20', '21'),
        ('21', 'B')
    ]
    
    for u, v in edges:
        maze.add_edge(u, v)
    
    heuristics = {
        'A': 8, '1': 6, '2': 6, '3': 6, '4': 7,
        '5': 4, '6': 12, '7': 7, '8': 15, '9': 18,
        '10': 6, '11': 8, '12': 6, '13': 5, '14': 4,
        '15': 8, '16': 6, '17': 3, '18': 5, '19': 5,
        '20': 2, '21': 1, 'B': 0
    }
    
    for node, value in heuristics.items():
        maze.set_heuristic(node, value)
    
    return maze

def get_maze_layout():
    layout = {
        'A': {'row': 7, 'col': 1},
        '1': {'row': 7, 'col': 4},
        '2': {'row': 5, 'col': 4},
        '3': {'row': 5, 'col': 2},
        '4': {'row': 5, 'col': 5},
        '5': {'row': 3, 'col': 2},
        '6': {'row': 3, 'col': 1},
        '7': {'row': 3, 'col': 3},
        '8': {'row': 1, 'col': 1},
        '9': {'row': 1, 'col': 3},
        '10': {'row': 2, 'col': 5},
        '11': {'row': 1, 'col': 5},
        '12': {'row': 2, 'col': 6},
        '13': {'row': 2, 'col': 7},
        '14': {'row': 3, 'col': 7},
        '15': {'row': 7, 'col': 7},
        '16': {'row': 7, 'col': 12},
        '17': {'row': 3, 'col': 9},
        '18': {'row': 1, 'col': 9},
        '19': {'row': 1, 'col': 10},
        '20': {'row': 5, 'col': 9},
        '21': {'row': 5, 'col': 12},
        'B': {'row': 1, 'col': 12}
    }
    
    walls = [
    
    ]
    
    return {'layout': layout, 'walls': walls}

# Flask routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/maze', methods=['GET'])
def get_maze():
    maze_layout = get_maze_layout()
    return jsonify(maze_layout)

@app.route('/api/solve', methods=['POST'])
def solve_maze():
    data = request.json
    
    algorithm = data.get('algorithm', 'bfs')
    start = data.get('start', 'A')
    goal = data.get('goal', 'B')
    
    # Create maze
    maze = create_maze()
    
    if algorithm == 'bfs':
        explored_path, solution_path = maze.breadth_first_search(start, goal)
        algorithm_name = "Breadth-First Search"
    elif algorithm == 'dfs':
        explored_path, solution_path = maze.depth_first_search(start, goal)
        algorithm_name = "Depth-First Search"
    elif algorithm == 'astar':
        explored_path, solution_path = maze.a_star_search(start, goal)
        algorithm_name = "A* Search"
    else:
        return jsonify({"error": "Invalid algorithm specified"}), 400
    
    response = {
        "algorithm": algorithm_name,
        "explored_path": explored_path,
        "solution_path": solution_path,
        "solution_length": len(solution_path) - 1 if solution_path else 0
    }
    
    return jsonify(response)

@app.route('/api/move', methods=['POST'])
def move_robot():
    data = request.json
    current_position = data.get('position')
    direction = data.get('direction')  # 'left', 'right', 'up', 'down'
    
    maze = create_maze()
    neighbors = [n for n, _ in maze.get_neighbors(current_position)]
    
 
    if not neighbors:
        return jsonify({"error": "No possible moves from current position"}), 400
    
     new_position = neighbors[0]
    
    return jsonify({"new_position": new_position})

@app.route('/templates/index.html')
def get_index_template():
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Robot Maze Navigation</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body {
                font-family: 'Arial', sans-serif;
                padding: 20px;
                background-color: #f5f5f5;
            }
            
            .maze-container {
                display: grid;
                grid-template-columns: repeat(12, 70px);
                grid-template-rows: repeat(7, 70px);
                gap: 2px;
                margin: 20px auto;
                background-color: #333;
            }
            
            .cell {
                background-color: white;
                display: flex;
                justify-content: center;
                align-items: center;
                font-weight: bold;
                position: relative;
                transition: background-color 0.3s;
            }
            
            .cell.path {
                background-color: #aaffaa;
            }
            
            .cell.explored {
                background-color: #ffffaa;
            }
            
            .cell.current {
                background-color: #ffaaaa;
            }
            
            .robot {
                position: absolute;
                width: 30px;
                height: 30px;
                background-color: #0066ff;
                border-radius: 50%;
                display: flex;
                justify-content: center;
                align-items: center;
                color: white;
                font-size: 18px;
                transition: transform 0.5s;
            }
            
            .control-panel {
                margin: 20px auto;
                max-width: 600px;
                background-color: white;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            }
            
            .move-controls {
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                grid-template-rows: repeat(3, 1fr);
                gap: 5px;
                max-width: 200px;
                margin: 20px auto;
            }
            
            .move-btn {
                padding: 10px;
                font-size: 18px;
            }
            
            .btn-left {
                grid-column: 1;
                grid-row: 2;
            }
            
            .btn-up {
                grid-column: 2;
                grid-row: 1;
            }
            
            .btn-right {
                grid-column: 3;
                grid-row: 2;
            }
            
            .btn-down {
                grid-column: 2;
                grid-row: 3;
            }
            
            .wall {
                position: absolute;
                background-color: #333;
            }
            
            .wall-horizontal {
                height: 4px;
                width: 100%;
            }
            
            .wall-vertical {
                width: 4px;
                height: 100%;
            }
            
            .wall-top {
                top: 0;
                left: 0;
            }
            
            .wall-bottom {
                bottom: 0;
                left: 0;
            }
            
            .wall-left {
                left: 0;
                top: 0;
            }
            
            .wall-right {
                right: 0;
                top: 0;
            }
            
            .status-panel {
                margin-top: 20px;
                padding: 10px;
                background-color: #f8f9fa;
                border-radius: 5px;
            }
            
            .cell-label {
                position: absolute;
                bottom: 5px;
                right: 5px;
                font-size: 12px;
                color: #666;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1 class="text-center mb-4">Robot Maze Navigation</h1>
            <h4 class="text-center mb-4">Made by Malak Aouragh and Malak benseid</h4>
            
            <div class="row">
                <div class="col-md-8">
                    <div class="maze-container" id="maze">
                   
                        
                    </div>
                </div>
                
                <div class="col-md-4">
                    <div class="control-panel">
                        <h4>Control Panel</h4>
                        
                        <div class="mb-3">
                            <label for="algorithm" class="form-label">Select Algorithm</label>
                            <select class="form-select" id="algorithm">
                                <option value="bfs">Breadth-First Search</option>
                                <option value="dfs">Depth-First Search</option>
                                <option value="astar">A* Search</option>
                            </select>
                        </div>
                        
                        <button id="findPathBtn" class="btn btn-primary w-100">Find Path</button>
                        
                        <div class="move-controls">
                            <button class="btn btn-secondary move-btn btn-left" id="moveLeft">←</button>
                            <button class="btn btn-secondary move-btn btn-right" id="moveRight">→</button>
                        </div>
                        
                        <button id="resetBtn" class="btn btn-danger w-100 mt-3">Reset</button>
                        
                        <div class="status-panel">
                            <p><strong>Current Position:</strong> <span id="currentPosition">A</span></p>
                            <p><strong>Steps Taken:</strong> <span id="stepsTaken">0</span></p>
                            <div id="algorithmInfo"></div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <script>
            document.addEventListener('DOMContentLoaded', function() {
                // State variables
                let mazeLayout;
                let walls;
                let robotPosition = 'A';
                let goal = 'B';
                let stepsTaken = 0;
                let solutionPath = [];
                let exploredPath = [];
                let adjacencyList = {};
                let solutionStepIndex =1;
                let manualPathConnectors = [
        'connector_1', 'connector_2', 'connector_7', 
        'connector_14',  'connector_16',
        'connector_17', 'connector_18', 'connector_19', 'connector_20',
        'connector_21','connector_11','connector_12'

    ];

                
                // Fetch maze layout
                fetchMazeLayout();
                
                // Event listeners
                document.getElementById('findPathBtn').addEventListener('click', findPath);
                document.getElementById('resetBtn').addEventListener('click', resetMaze);
                document.getElementById('moveLeft').addEventListener('click', () => moveBackAlongSolution());
                document.getElementById('moveRight').addEventListener('click', () => moveAlongSolution());

                function fetchMazeLayout() {
                    fetch('/api/maze')
                        .then(response => response.json())
                        .then(data => {
                            mazeLayout = data.layout;
                            walls = data.walls;

                            mazeLayout['connector_1'] = { row: 7, col: 2 }; 
                            mazeLayout['connector_2'] = { row: 7, col: 3 }; 
                            mazeLayout['connector_3'] = { row: 7, col: 8 }; 
                            mazeLayout['connector_4'] = { row: 7, col: 9 }; 
                            mazeLayout['connector_5'] = { row: 7, col: 10 }; 
                            mazeLayout['connector_6'] = { row: 7, col: 11}; 
                            mazeLayout['connector_7'] = { row: 6, col: 4 }; 
                            mazeLayout['connector_8'] = { row: 6, col: 7 }; 
                            mazeLayout['connector_9'] = { row: 5, col: 3 }; 
                            mazeLayout['connector_10'] = { row: 5, col: 7 }; 
                            mazeLayout['connector_11'] = { row: 5, col: 11 }; 
                            mazeLayout['connector_12'] = { row: 5, col: 10}; 
                            mazeLayout['connector_13'] = { row: 4 , col: 2 }; 
                            mazeLayout['connector_14'] = { row: 4, col: 5 }; 
                            mazeLayout['connector_15'] = { row: 4, col: 7 }; 
                            mazeLayout['connector_16'] = { row: 4, col: 9 }; 
                            mazeLayout['connector_17'] = { row: 4, col: 12 }; 
                            mazeLayout['connector_18'] = { row: 3, col: 12 }; 
                            mazeLayout['connector_19'] = { row: 3, col: 8 }; 
                            mazeLayout['connector_20'] = { row: 3, col: 5 }; 
                            mazeLayout['connector_21'] = { row: 2, col: 12 }; 
                            mazeLayout['connector_22'] = { row: 2, col: 9 }; 
                            mazeLayout['connector_23'] = { row: 2, col: 1 }; 
                            mazeLayout['connector_24'] = { row: 2, col: 3 }; 
                            
                        
                            
                            // Render the maze
                            renderMaze();
                            
                            // Update robot position
                            updateRobotPosition('A');
                        })
                        .catch(error => console.error('Error fetching maze layout:', error));
                }
                
              
                function renderMaze() {
                    const mazeContainer = document.getElementById('maze');
                    mazeContainer.innerHTML = '';
                    
                    const grid = Array(8).fill().map(() => Array(12).fill(null));
                    
                    // Place cells in the grid
                    for (let cellId in mazeLayout) {
                        const { row, col } = mazeLayout[cellId];
                        
                        const cell = document.createElement('div');
                        cell.className = 'cell';
                        cell.id = `cell-${cellId}`;
                        cell.dataset.id = cellId;
                        
                
        const isConnector = cellId.startsWith('connector_');
        
        if (!isConnector) {
            // Add cell label for nodes
            const label = document.createElement('div');
            label.className = 'cell-label';
            label.textContent = cellId;
            cell.appendChild(label);
        } else {
            // Style connector cells differently
                        const label = document.createElement('div');
                        label.textContent = '';
                        cell.class = `cell-${cellId}`;


        }
        
                        
                        // Position the cell in the grid
                        cell.style.gridRow = row;
                        cell.style.gridColumn = col;
                        
                        mazeContainer.appendChild(cell);
                        grid[row][col] = cellId;
                    }
                    
                    // Add robot element
                    const robotElement = document.createElement('div');
                    robotElement.className = 'robot';
                    robotElement.id = 'robot';
                    robotElement.textContent = '🤖';
                    document.getElementById(`cell-${robotPosition}`).appendChild(robotElement);
                    
                    // Highlight start and goal
                    document.getElementById('cell-A').style.backgroundColor = '#ccffcc';
                    document.getElementById('cell-B').style.backgroundColor = '#ffcccc';
                }
                
                function findPath() {
                    const algorithm = document.getElementById('algorithm').value;
                    
                    // Reset previous path
                    clearPathHighlight();
                    
                    // Send request to backend
                    fetch('/api/solve', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({
                            algorithm: algorithm,
                            start: robotPosition,
                            goal: goal
                        })
                    })
                    .then(response => response.json())
                    .then(data => {
                        // Store paths
                        solutionPath = data.solution_path;
                        exploredPath = data.explored_path;
                        
                        
                        // Display algorithm info
                        document.getElementById('algorithmInfo').innerHTML = `
                            <p><strong>${data.algorithm}</strong></p>
                            <p>Solution Path: ${solutionPath.join(' → ')}</p>
                            <p>Explored Path: ${exploredPath.join(' → ')}</p>
                            <p>Path Length: ${data.solution_length} steps</p>
                        `;
                        
                        // Highlight paths
                        highlightPath();
                    })
                    .catch(error => console.error('Error finding path:', error));
                }
                
                                
                function clearPathHighlight() {
                    document.querySelectorAll('.cell').forEach(cell => {
                        cell.classList.remove('path', 'explored');
                    });
                    
                    // Reset start and goal colors
                    document.getElementById('cell-A').style.backgroundColor = '#ccffcc';
                    document.getElementById('cell-B').style.backgroundColor = '#ffcccc';
                }
                
             
                function updateRobotPosition(newPosition) {
                    // Update state
                    robotPosition = newPosition;
                    document.getElementById('currentPosition').textContent = robotPosition;
                    
                    // Move robot element
                    const robotElement = document.getElementById('robot');
                    if (robotElement.parentNode) {
                        robotElement.parentNode.removeChild(robotElement);
                    }
                    
                    const newCell = document.getElementById(`cell-${newPosition}`);
                    newCell.appendChild(robotElement);
                    
                    // Highlight current position
                    document.querySelectorAll('.cell').forEach(cell => {
                        cell.classList.remove('current');
                    });
                    newCell.classList.add('current');
                }
                function highlightPath() {
        exploredPath.forEach(cellId => {
            const cell = document.getElementById(`cell-${cellId}`);
            if (cell && cellId !== robotPosition && cellId !== goal) {
                cell.classList.add('explored');
            }
        });

        solutionPath.forEach(cellId => {
            const cell = document.getElementById(`cell-${cellId}`);
            if (cell && cellId !== robotPosition && cellId !== goal) {
                cell.classList.add('solution');
                cell.style.backgroundColor = 'lightgreen'; // Highlight solution path in green
            }
        });
        manualPathConnectors.forEach(connectorId => {
        console.log(connectorId);
        const connectorElement = document.getElementById(`cell-${connectorId}`);
        if (!connectorElement) {
            console.warn(`Element not found: cell-${connectorId}`);
        } else {
            connectorElement.classList.add('path');
        }
    });
    }
    
    function moveAlongSolution() {
        console.log(solutionPath);
        console.log(solutionStepIndex);

        if (solutionStepIndex < solutionPath.length) {
            updateRobotPosition(solutionPath[solutionStepIndex]);
            stepsTaken++;
            document.getElementById('stepsTaken').textContent = stepsTaken;
            solutionStepIndex++;

            if (robotPosition === goal) {
                setTimeout(() => alert('Congratulations! You reached the goal!'), 500);
            }
        } else {
            alert('You have reached the goal!');
            solutionStepIndex = 0;
        }
    }

    function moveBackAlongSolution() {
    if (solutionStepIndex > 0) {
        solutionStepIndex--; // Move to the previous step
        updateRobotPosition(solutionPath[solutionStepIndex]);
        stepsTaken++;
        document.getElementById('stepsTaken').textContent = stepsTaken;

        if (robotPosition === start) {
            setTimeout(() => alert('You are back at the start!'), 500);
        }
    } else {
        alert('You are already at the start!');
    }
}
    
    function updateRobotPosition(newPosition) {
        robotPosition = newPosition;
        document.getElementById('currentPosition').textContent = robotPosition;
        
        const robotElement = document.getElementById('robot');
        if (robotElement.parentNode) {
            robotElement.parentNode.removeChild(robotElement);
        }

        const newCell = document.getElementById(`cell-${newPosition}`);
        newCell.appendChild(robotElement);
        document.querySelectorAll('.cell').forEach(cell => cell.classList.remove('current'));
        newCell.classList.add('current');
    }
    
    function clearPathHighlight() {
        document.querySelectorAll('.cell').forEach(cell => {
            cell.classList.remove('path', 'explored', 'solution');
            cell.style.backgroundColor = ''; // Reset background color
        });

        document.getElementById('cell-A').style.backgroundColor = '#ccffcc';
        document.getElementById('cell-B').style.backgroundColor = '#ffcccc';
    }
    
                
                function resetMaze() {
                    // Reset robot position
                    updateRobotPosition('A');
                    
                    // Reset steps
                    stepsTaken = 0;
                    document.getElementById('stepsTaken').textContent = stepsTaken;
                    
                    // Clear path highlights
                    clearPathHighlight();
                    
                    // Clear algorithm info
                    document.getElementById('algorithmInfo').innerHTML = '';
                    
                    // Reset solution and explored paths
                    solutionPath = [];
                    exploredPath = [];
                }
            });

            
        </script>
    </body>
    </html>
    """
    return html_content

@app.route('/templates/<path:filename>')
def serve_template(filename):
    return get_index_template()

if __name__ == '__main__':
    # Make sure templates directory exists
    if not os.path.exists('templates'):
        os.makedirs('templates')
    
template_path = os.path.join('templates', 'index.html')
if not os.path.exists(template_path):
    with open(template_path, 'w', encoding='utf-8') as f: 
        f.write(get_index_template())  

app.run(debug=True)
