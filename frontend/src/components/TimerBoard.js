import "./Kanban.css";
import TimerCard from "./TimerCard";

function TimerBoard({ boardName, timers, onClickComplete }) {
  return (
    <div className="kanban-board">
      <h3 className="board-name">{boardName}</h3>
      {timers.map((timer, id) => (
        <TimerCard
          className={timer.completed_at ? "completed-card" : "ongoing-card"}
          key={id}
          timer={timer}
          onClickComplete={onClickComplete}
        />
      ))}
    </div>
  );
}

export default TimerBoard;
