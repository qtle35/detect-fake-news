import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Home from './components/home';
import Maus from './components/mau';
import MauDetail from './components/mauDetail';

function App() {
  return (
    <BrowserRouter>
      {/* <Navbar /> */}
      <Routes>
        <Route path='/' element={<Home />} />
        <Route path='/maus' element={<Maus />} />
        <Route path='/mau/:id' element={<MauDetail />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
