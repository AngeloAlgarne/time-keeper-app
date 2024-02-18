import "./Kanban.css";

import { msToHours, formatDate } from "../utilityFunctions";

function TimerCard({ className, timer, completed }) {

  const SmallNote = () => {
    return (
      <p className="small-font">
        Started at {formatDate(timer.created_at, true)}
        {completed ? (
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

  return (
    <div className={className + " kanban-card"}>
      <h2>{timer.project_name}</h2>
      <h3 className="badge">{msToHours(timer.duration_ms)} hours</h3>
      <p>{timer.project_description}</p>
      <SmallNote />
    </div>
  );
}

export default TimerCard;
