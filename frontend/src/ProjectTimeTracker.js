import React from "react";
import axios from "axios";

import Kanban from "./components/Kanban";
import Board from "./components/KanbanBoard";
import Card from "./components/KanbanCard";

class ProjectTimeTracker extends React.Component {
  state = { projects: [], timers: [], onhold: [] };

  componentDidMount() {
    let projectsUrl = "http://localhost:8000/projects";
    let timersUrl = "http://localhost:8000/timers";
    let onholdUrl = "http://localhost:8000/onhold";

    axios
      // Fetch all projects
      .get(projectsUrl)
      .then((response) => {
        this.setState({
          ...this.state,
          projects: response.data,
        });
        // Fetch all projects with timers
        return axios.get(timersUrl);
      })
      .then((response) => {
        this.setState({
          ...this.state,
          timers: response.data,
        });
        // Fetch all onhold project timers
        return axios.get(onholdUrl);
      })
      .then((response) => {
        this.setState({
          ...this.state,
          onhold: response.data,
        });
      })
      .catch((error) => {});
  }

  render() {
    return (
      <Kanban kanbanName={"Project Time Tracker"}>
        <Board boardName={"Projects"}>
          {this.state.projects.map((project, id) => (
            <Card>
              <div key={id}>
                <h2>{project.name}</h2>
                <p>{project.description}</p>
                <p className="small-font">Created at {project.created_at}</p>
              </div>
            </Card>
          ))}
        </Board>
        <Board boardName={"Ongoing"}>
          <Card className="ongoing-card">
            {this.state.timers.map((timer, id) => (
              <div key={id}>
                <h2>{timer.project_name}</h2>
                <h3>{timer.duration}</h3>
                <p>{timer.project_description}</p>
                <p className="small-font">
                  Created at {timer.project_created_at}
                </p>
                <p className="small-font">
                  Timer started at {timer.timer_created_at}
                </p>
              </div>
            ))}
          </Card>
        </Board>
        <Board boardName={"On Hold"}>
          <Card className="onhold-card">
            {this.state.onhold.map((timer, id) => (
              <div key={id}>
                <h2>{timer.project_name}</h2>
                <h3>{timer.duration}</h3>
                <p>{timer.project_description}</p>
                <p className="small-font">
                  Created at {timer.project_created_at}
                </p>
                <p className="small-font">
                  Timer started at {timer.timer_created_at}
                </p>
              </div>
            ))}
          </Card>
        </Board>
      </Kanban>
    );
  }
}

export default ProjectTimeTracker;
