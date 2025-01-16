import { Card, CardContent, CardHeader, LinearProgress, Typography } from "@mui/material";

import OpacityIcon from "@mui/icons-material/Opacity";
import ThermostatIcon from "@mui/icons-material/Thermostat";
import WbSunnyIcon from "@mui/icons-material/WbSunny";
import { useBackend } from "@/services/backend";

interface Props {
    title: string;
    id: string;
}
export const PlantationCard: React.FC<Props> = ({ title, id }) => {
    const {
        data: plantation,
        isLoading,
        error,
    } = useBackend("/api/plantation", { plantationUUID: id });
    return (
        <Card>
            <CardHeader title={title} />
            <CardContent>
                {isLoading && <LinearProgress />}
                {error && "error"}
                {plantation && <PlantationSensors />}
            </CardContent>
        </Card>
    );
};

interface SensorProps {}
const PlantationSensors: React.FC<SensorProps> = () => {
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
