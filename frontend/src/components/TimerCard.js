import "./Kanban.css";

import { secondsToHours, formatDate } from "../utilityFunctions";

function TimerCard({ className, timer, onClickComplete }) {
  const hoursDisplay = (hours) => {
    if (hours == 1) {
      return `${hours} hour`;
    }
    return `${hours} hours`;
  };

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
          <button onClick={() => onClickComplete(timer.id)}>Complete</button>
        )}
      </div>
    );
  };

  return (
    <div className={className + " kanban-card"}>
      <h2>{timer.project_name}</h2>
      <h3 className="badge">{hoursDisplay(secondsToHours(timer.duration_seconds))}</h3>
      <p>{timer.project_description}</p>
      <SmallNote />
      <Buttons />
    </div>
  );
}

export default TimerCard;
