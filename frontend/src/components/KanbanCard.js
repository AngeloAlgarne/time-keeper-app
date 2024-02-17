import './Kanban.css'

function Card({ children }) {
    return (
      <div className="kanban-card">
        {children}
      </div>
    );
  }
  
  export default Card;