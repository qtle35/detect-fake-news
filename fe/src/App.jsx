import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Home from './components/home';
import Maus from './components/mau';
import MauDetail from './components/mauDetail';
import CustomSidebar from './components/sidebar';
import LabelPage from './components/label-page';
import LabelEdit from './components/label-edit';
import Login from './components/login';
import { AuthProvider } from './components/auth-context'
import PrivateRoute from './components/private-route'
import PredictLogPage from './components/predict-log';
import SelectSamples from './components/select-sample';

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <div className='grid grid-cols-6'>
          <div className='col-span-1'>
            <CustomSidebar />
          </div>
          <div className='col-span-5'>
            <main>
              <Routes>
                {/* <Route path="/home" element={<Home />} /> */}
                <Route path='/' element={<Home />} />
                <Route path='/login' element={<Login />} />
                <Route path='/label' element={<PrivateRoute><LabelPage /></PrivateRoute>} />
                <Route path='/label/:id' element={<PrivateRoute><LabelEdit /></PrivateRoute>} />
                <Route path='/maus' element={<Maus />} />
                <Route path='/mau/:id' element={<MauDetail />} />
                <Route path='/predict-log' element={<PredictLogPage />} />
                {/* <Route path='/selectsample' element={<SelectSamples />} /> */}
              </Routes>
            </main>
          </div>
        </div>
      </BrowserRouter>
    </AuthProvider>
  );
}

export default App;
