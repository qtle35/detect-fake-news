import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Home from './components/home';
import LabelPage from './components/label-page';
import React from 'react';
import LabelEdit from './components/label-edit';

function App() {
  return (
    <BrowserRouter>
      {/* <Navbar /> */}
      <Routes>
        <Route path='/' element={<Home />} />
        <Route path='/label' element={<LabelPage />} />
        <Route path='/label/:id' element={<LabelEdit />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
