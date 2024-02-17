import "./Kanban.css";

function Kanban({ kanbanName, children }) {
  return (
    <div className="kanban-container">
      <h1>{kanbanName}</h1>
      <div className="kanban">{children}</div>
    </div>
  );
}

export default Kanban;
