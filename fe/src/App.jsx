import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Home from './components/home';
import CustomSidebar from './components/sidebar';
function App() {
  return (
    <BrowserRouter>
      <div id="app" style={{ display: "flex"}}>
        <CustomSidebar/>
        <main>
          <Routes>
            <Route path="/home" element={<Home />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}

export default App;
