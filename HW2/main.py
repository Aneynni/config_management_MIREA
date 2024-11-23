#zxczxc
#!/bin/python3
import git
import argparse
from pathlib import Path

def get_commit_graph(repo_path):
    repo = git.Repo(repo_path)
    commits = list(repo.iter_commits('main'))
    graph = "graph TD;\n"

    for commit in commits:
        commit_id = commit.hexsha[:7]
        graph += f"    {commit_id}({commit_id});\n"
        for parent in commit.parents:
            parent_id = parent.hexsha[:7]
            graph += f"    {parent_id} --> {commit_id};\n"

    return graph

def save_graph_to_file(graph, output_path):
    with open(output_path, 'w') as f:
        f.write(graph)

def main():
    parser = argparse.ArgumentParser(description="Visualize git commit dependencies.")
    parser.add_argument('repo_path', type=str, help='Path to the git repository')
    parser.add_argument('output_path', type=str, help='Path to save the graph file')

    args = parser.parse_args()

    graph = get_commit_graph(args.repo_path)
    save_graph_to_file(graph, args.output_path)
    print(f"Graph saved to {args.output_path}")

if __name__ == "__main__":
    main()
