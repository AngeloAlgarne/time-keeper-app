import React from "react";
import axios from "axios";

import Kanban from "./components/Kanban";
import Board from "./components/KanbanBoard";
import Card from "./components/KanbanCard";
import TimerBoard from "./components/TimerBoard";

import { formatDate } from "./utilityFunctions";

const urls = {
  projects: "http://localhost:8000/projects",
  timers: "http://localhost:8000/timers",
  completed: "http://localhost:8000/completed",
};

export default class ProjectTimeTracker extends React.Component {
  state = { projects: [], timers: [], completed: [], newProject: {} };

  componentDidMount() {
    axios
      // Fetch all projects
      .get(urls.projects)
      .then((response) => {
        this.setState({
          ...this.state,
          projects: response.data,
        });
        // Fetch all projects with timers
        return axios.get(urls.timers);
      })
      .then((response) => {
        this.setState({
          ...this.state,
          timers: response.data,
        });
        // Fetch all completed projects
        return axios.get(urls.completed);
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
    const setNewProjectValue = (name, description) => {
      this.setState({
        ...this.state,
        newProject: {
          name: name,
          description: description,
        },
      });
    };

    const onChangeNewProjectName = (e) =>
      setNewProjectValue(e.target.value, this.state.newProject.description);
    const onChangeNewProjectDescription = (e) =>
      setNewProjectValue(this.state.newProject.name, e.target.value);

    const handleNewProject = (data) => {
      axios
        .post(urls.projects, {
          name: data.name,
          description: data.description,
        })
        .then((response) => {
          window.location.reload();
        });
    };

    const handleStart = (projectId) => {
      axios.post(urls.timers, { project: projectId }).then((response) => {
        window.location.reload();
      });
    };

    // const handlePause = () => {};
    // const handleResume = () => {};

    const handleComplete = (timerId) => {
      axios.put(urls.completed, { timer: timerId}).then((response) => {
        window.location.reload();
      });
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
                <div className="button-div">
                  <button onClick={() => handleStart(project.id)}>Start</button>
                </div>
              </div>
            </Card>
          ))}
          <Card>
            <form>
              <h2>New Project</h2>
              <div className="input-div">
                <input type="text" onChange={onChangeNewProjectName} placeholder="Name"/>
                <input type="text" onChange={onChangeNewProjectDescription} placeholder="Description"/>
              </div>
              <div className="button-div">
                <button onClick={() => handleNewProject(this.state.newProject)}>
                  Create
                </button>
              </div>
            </form>
          </Card>
        </Board>
        <TimerBoard
          boardName={"Ongoing"}
          timers={this.state.timers}
          onClickComplete={handleComplete}
        />
        <TimerBoard boardName={"Completed"} timers={this.state.completed} />
      </Kanban>
    );
  }
}
