import Globe3D from './components/Globe3D';
import RiskTable from './components/RiskTable';
import TimeScrubber from './components/TimeScrubber';

export default function App() {
  return <main><h1>Space Debris Dashboard</h1><Globe3D /><TimeScrubber /><RiskTable /></main>;
}
