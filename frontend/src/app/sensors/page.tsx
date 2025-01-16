import React from 'react';

const sensors = [
    { number: 1, description: 'Sensor #1', status: 'online' },
    { number: 2, description: 'Sensor #2', status: 'online' },
    { number: 3, description: 'Sensor #3', status: 'online' },
    { number: 4, description: 'Sensor #4', status: 'online' },
    { number: 5, description: 'Sensor #5', status: 'online' },
    { number: 6, description: 'Sensor #6', status: 'online' },
];

export default function Page() {
    return (
        <div>
            {sensors.map((sensor) => (
                <div key={sensor.number} style={{ backgroundColor: 'normal', padding: '10px', margin: '10px' }}>
                    <h2>{sensor.description}</h2>
                    <div style={{ width: '10px', height: '10px', borderRadius: '50%', backgroundColor: 'green', animation: 'pulse 1s infinite' }}></div>
                    <p>Status: {sensor.status}</p>
                </div>
            ))}
        </div>
    );
}
