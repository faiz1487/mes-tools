import React, { useEffect, useState } from 'react'

function LineMonitor(){
  const [wsLog, setWsLog] = useState([])
  useEffect(()=>{
    const url = (location.protocol === 'https:' ? 'wss://' : 'ws://') + (location.hostname || 'localhost') + ':8000' + '/ws/line/line-1'
    const ws = new WebSocket(url)
    ws.onopen = ()=> ws.send(JSON.stringify({event:'subscribe', line:'line-1'}))
    ws.onmessage = (ev)=> setWsLog(l => [ev.data, ...l].slice(0,50))
    return ()=> ws.close()
  },[])
  return (
    <div className="p-4 border rounded bg-white">
      <h3 className="text-lg font-semibold">Line Monitor (real-time)</h3>
      <ul className="text-sm mt-2 max-h-48 overflow-auto">
        {wsLog.map((l,i)=>(<li key={i}>{l}</li>))}
      </ul>
    </div>
  )
}

function Traceability(){
  const [serial, setSerial] = useState('SN1001')
  const [records, setRecords] = useState([])
  async function query(){
    const r = await fetch(`/api/trace/${serial}`)
    const j = await r.json()
    setRecords(j)
  }
  useEffect(()=>{ query() }, [])
  return (
    <div className="p-4 bg-white rounded border">
      <h3 className="text-lg font-semibold">Traceability</h3>
      <div className="mt-2 flex">
        <input value={serial} onChange={e=>setSerial(e.target.value)} placeholder="Enter serial" className="border p-2 flex-1" />
        <button onClick={query} className="ml-2 px-3 py-2 rounded bg-slate-700 text-white">Lookup</button>
      </div>
      <div className="mt-4">
        {records.length===0? <p className="text-sm">No records</p> : (
          <table className="min-w-full table-auto">
            <thead><tr><th>Station</th><th>Status</th><th>Time</th></tr></thead>
            <tbody>
              {records.map(r=> (
                <tr key={r.id}><td>{r.station}</td><td>{r.status}</td><td>{new Date(r.timestamp).toLocaleString()}</td></tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  )
}

export default function App(){
  return (
    <div className="p-6 font-sans min-h-screen bg-slate-100">
      <h1 className="text-2xl font-bold">MES Starter — Mobile Manufacturing (Full)</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4">
        <LineMonitor />
        <Traceability />
      </div>
    </div>
  )
}
