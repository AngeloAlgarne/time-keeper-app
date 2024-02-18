import React from "react";
import axios from "axios";

import Kanban from "./components/Kanban";
import Board from "./components/KanbanBoard";
import Card from "./components/KanbanCard";

class ProjectTimeTracker extends React.Component {
  state = { projects: [], timers: [], onhold: [], completed: [] };

  componentDidMount() {
    let projectsUrl = "http://localhost:8000/projects";
    let timersUrl = "http://localhost:8000/timers";
    let onholdUrl = "http://localhost:8000/onhold";
    let completedUrl = "http://localhost:8000/onhold";

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
        // Fetch all completed projects
        return axios.get(completedUrl);
      })
      .then((response) => {
        this.setState({
          ...this.state,
          completed: response.data,
        });
      })
      .catch((error) => {});
  }

  render() {
    const msToHours = (milliseconds) => {
      let seconds = Math.floor(milliseconds / 1000);
      let minutes = Math.floor(seconds / 60);
      let hours = Math.floor(minutes / 60);
      return hours;
    };

    const formatDate = (dateString, withTime) => {
      let options = {
        year: "numeric",
        month: "numeric",
        day: "numeric",
      };

      if (withTime) {
        options.hour = "numeric";
        options.minute = "numeric";
      }

      return new Date(dateString).toLocaleString("en-US", options);
    };

    return (
      <Kanban kanbanName={"Project Time Tracker"}>
        <Board boardName={"Projects"}>
          {this.state.projects.map((project, id) => (
            <Card key={id}>
              <div>
                <h2>{project.name}</h2>
                <p>{project.description}</p>
                <p className="small-font">
                  Created on {formatDate(project.created_at)}
                </p>
              </div>
            </Card>
          ))}
        </Board>
        <Board boardName={"Ongoing"}>
          {this.state.timers.map((timer, id) => (
            <Card className={timer.onhold ? "" : "ongoing-card"} key={id}>
              <div>
                <h2>{timer.project_name}</h2>
                <h3 className="badge">{msToHours(timer.duration_ms)} hours</h3>
                <p>{timer.project_description}</p>
                <p className="small-font">
                  Started at {formatDate(timer.created_at, true)}
                  <br></br>
                  Created on {formatDate(timer.project_created_at)}
                </p>
              </div>
            </Card>
          ))}
        </Board>
        <Board boardName={"Completed"}>
          {this.state.completed.map((timer, id) => (
            <Card className="completed-card" key={id}>
              <div>
                <h2>{timer.project_name}</h2>
                <h3 className="badge">{msToHours(timer.duration)} hours</h3>
                <p>{timer.project_description}</p>
                <p className="small-font">
                  Started at {formatDate(timer.created_at, true)}
                  <br></br>
                  Completed at {formatDate(timer.completed_at, true)}
                  <br></br>
                  Created on {formatDate(timer.project_created_at)}
                </p>
              </div>
            </Card>
          ))}
        </Board>
      </Kanban>
    );
  }
}

export default ProjectTimeTracker;
