from flask import Flask, jsonify, render_template
import osmnx as ox
import networkx as nx
from shapely.geometry import Point
import random
from datetime import datetime

app = Flask(__name__)

# GeoAreaの定義（指定されたエリア）
GEOAREA = {
    "min_latitude": 36.55417135941204,
    "max_latitude": 36.56335803908794,
    "min_longitude": 139.89964199794943,
    "max_longitude": 139.91815996901008
}

# 道路ネットワークをグラフとして取得
G = ox.graph_from_bbox(GEOAREA['max_latitude'], GEOAREA['min_latitude'], GEOAREA['max_longitude'], GEOAREA['min_longitude'], network_type='walk')

# グラフのノードからターゲットの初期位置を決定
start_node = random.choice(list(G.nodes))
target_position = Point(G.nodes[start_node]['x'], G.nodes[start_node]['y'])

# 位置履歴を保存するリスト
position_history = [target_position]
visited_nodes = {start_node}  # 訪れたノードを記録するセット

def move_target(current_node, visited_nodes, G):
    # 訪れたことのない隣接ノードを選択
    neighbors = list(G.neighbors(current_node))
    unvisited_neighbors = [node for node in neighbors if node not in visited_nodes]
    
    if not unvisited_neighbors:  # もし未訪問のノードがない場合、訪問済みノードから選択
        unvisited_neighbors = neighbors
    
    next_node = random.choice(unvisited_neighbors)

    # ダイクストラ法で最短経路を計算
    path = nx.shortest_path(G, current_node, next_node, weight='length')

    # 次のノードに移動
    next_position = Point(G.nodes[path[1]]['x'], G.nodes[path[1]]['y'])
    visited_nodes.add(next_node)  # 訪れたノードとして記録
    return path[1], next_position

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/location', methods=['GET'])
def get_location():
    global start_node, target_position, position_history, visited_nodes
    start_node, target_position = move_target(start_node, visited_nodes, G)
    position_history.append(target_position)
    # 現在時刻を取得
    current_time = datetime.now().isoformat()

    return jsonify({
        'latitude': target_position.y,
        'longitude': target_position.x,
        'timestamp': current_time  # 時刻を追加
    })

@app.route('/history', methods=['GET'])
def get_history():
    global position_history
    history = [{'latitude': pos.y, 'longitude': pos.x} for pos in position_history]
    return jsonify(history)

if __name__ == '__main__':
    app.run(debug=True)
