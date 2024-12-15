import { Card, CardContent, CardHeader, Typography } from "@mui/material"

import OpacityIcon from '@mui/icons-material/Opacity';
import ThermostatIcon from '@mui/icons-material/Thermostat';
import WbSunnyIcon from '@mui/icons-material/WbSunny';

interface Props {
    title: string;
}
export const PlantationCard: React.FC<Props> = ({title}) => {
    return <Card>
        <CardHeader title={title} />
        <CardContent>
            <Typography variant="h5"><ThermostatIcon/> 21°C</Typography>
            <Typography variant="h5"><OpacityIcon/> 25%</Typography>
            <Typography variant="h5"><WbSunnyIcon/> 800lm</Typography>
        </CardContent>
    </Card>
}