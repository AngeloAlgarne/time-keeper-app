import './Kanban.css'

function Card({ className, children }) {
    return (
      <div className={className + " kanban-card"}>
        {children}
      </div>
    );
  }
  
  export default Card;