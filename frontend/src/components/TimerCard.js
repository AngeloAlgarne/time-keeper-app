import "./Kanban.css";

import { msToHours, formatDate } from "../utilityFunctions";

function TimerCard({ className, timer, onClickComplete }) {
  const SmallNote = () => {
    return (
      <p className="small-font">
        Started at {formatDate(timer.created_at, true)}
        {timer.completed_at ? (
          <>
            <br></br>
            Completed at {formatDate(timer.completed_at, true)}
          </>
        ) : (
          <></>
        )}
        <br></br>
        Created on {formatDate(timer.project_created_at)}
      </p>
    );
  };

  const Buttons = () => {
    return (
      <div className="button-div">
        {timer.completed_at ? (
          <></>
        ) : (
          <button onClick={onClickComplete}>Complete</button>
        )}
      </div>
    );
  };

  return (
    <div className={className + " kanban-card"}>
      <h2>{timer.project_name}</h2>
      <h3 className="badge">{msToHours(timer.duration_ms)} hours</h3>
      <p>{timer.project_description}</p>
      <SmallNote />
      <Buttons />
    </div>
  );
}

export default TimerCard;
