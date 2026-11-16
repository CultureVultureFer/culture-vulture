import Header from "../Header"
import Footer from "../Footer"
import Filters from "../Filters"
import Events from "../Events"


function HomePage() {
 
  return(
    <>
    <Header></Header>
    
    <main>
      <Filters></Filters>
      <Events></Events>
    </main>
    <Footer></Footer>
    </>
    
  )
}

export default HomePage