import React from "react";
import axios from "axios";

import Kanban from "./components/Kanban";
import Board from "./components/KanbanBoard";
import Card from "./components/KanbanCard";
import TimerBoard from "./components/TimerBoard";

import { formatDate } from "./utilityFunctions";

export default class ProjectTimeTracker extends React.Component {
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
    const handleStart = () => {};

    const handlePause = () => {};

    const handleResume = () => {};

    const handleComplete = () => {};

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
                <div className="button-div">
                  <button onClick={handleStart}>Start</button>
                </div>
              </div>
            </Card>
          ))}
        </Board>
        <TimerBoard
          boardName={"Ongoing"}
          timers={this.state.timers}
          onClickComplete={handleComplete}
        />
        <TimerBoard
          boardName={"Completed"}
          timers={this.state.completed}
        />
      </Kanban>
    );
  }
}
