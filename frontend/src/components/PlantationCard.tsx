import { Card, CardContent, CardHeader, LinearProgress, Typography } from "@mui/material";

import OpacityIcon from "@mui/icons-material/Opacity";
import ThermostatIcon from "@mui/icons-material/Thermostat";
import WbSunnyIcon from "@mui/icons-material/WbSunny";
import { useBackend, useSSE } from "@/services/backend";
import { PlantationDetails, SensorUpdate } from "@/types/rest";

interface Props {
    title: string;
    id: string;
}

//plantacja: pogodowe, token, sensory na bieżąco, podlewanie, historyczne dane z sensorów na wykresie z endpointu /api/sensorsdata
export const PlantationCard: React.FC<Props> = ({ title, id }) => {
    const {
        data: plantation,
        isLoading,
        error,
    } = useBackend<PlantationDetails>("/api/plantation", { plantationUUID: id });
    return (
        <Card>
            <CardHeader title={title} />
            <CardContent>
                {isLoading && <LinearProgress />}
                {error && "error"}
                {plantation && <PlantationSensors plantationid={id}/>}
            </CardContent>
        </Card>
    );
};

interface SensorProps {
    plantationid: string;
}
const PlantationSensors: React.FC<SensorProps> = ({plantationid}) => {
    const sensorValues = useSSE<SensorUpdate>('/api/sensors', {plantationUUID: plantationid}) ?? [];
    console.log(sensorValues);
    return (
        <>
            <Typography variant="h5">
                <ThermostatIcon /> 21°C
            </Typography>
            <Typography variant="h5">
                <OpacityIcon /> 25%
            </Typography>
            <Typography variant="h5">
                <WbSunnyIcon /> 800lm
            </Typography>
        </>
    );
};
