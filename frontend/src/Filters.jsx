import "./Filters.css"
function Filters(){
    return(
        <>
        <h1 className="h1">Events happening near you</h1>

        <div className="fildiv">
            <p1 className="spanbuttons">Filters: </p1>
            <button className="buttons">Date</button>
            <button className="buttons">Price</button>
            <button className="buttons">Distance</button>

        </div>
        <hr className="line"></hr>
        </>
    )
}
export default Filters