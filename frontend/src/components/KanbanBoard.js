import "./Kanban.css";

function Board({ boardName, children }) {
  return (
    <div className="kanban-board">
      <h3 className="board-name">{boardName}</h3>
      <div>{children}</div>
    </div>
  );
}

export default Board;
