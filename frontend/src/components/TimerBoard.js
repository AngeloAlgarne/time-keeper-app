import "./Kanban.css";
import TimerCard from "./TimerCard";

function TimerBoard({ boardName, timers }) {
  return (
    <div className="kanban-board">
      <h3 className="board-name">{boardName}</h3>
      {timers.map((timer, id) => (
        <TimerCard
          className={timer.onhold ? "" : "ongoing-card"}
          key={id}
          timer={timer}
        />
      ))}
    </div>
  );
}

export default TimerBoard;
