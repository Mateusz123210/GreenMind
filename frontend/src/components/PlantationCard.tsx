import {
    Button,
    Card,
    CardContent,
    CardHeader,
    CircularProgress,
    Dialog,
    DialogActions,
    DialogContent,
    DialogTitle,
    InputAdornment,
    LinearProgress,
    Stack,
    TextField,
    Typography,
} from "@mui/material";

import OpacityIcon from "@mui/icons-material/Opacity";
import ThermostatIcon from "@mui/icons-material/Thermostat";
import WbSunnyIcon from "@mui/icons-material/WbSunny";
import { deleteBackend, postBackend, useBackend, useSensorUpdate } from "@/services/backend";
import { PlantationDetails } from "@/types/rest";
import { FormEvent, useMemo, useState } from "react";
import CopyAllIcon from "@mui/icons-material/CopyAll";
import { DateTimePicker } from "@mui/x-date-pickers";
import dayjs from "dayjs";
import { RemoveButton } from "./RemoveButton";
import { mutate as globalMutate } from "swr";

interface Props {
    title: string;
    id: string;
}

//plantacja: pogodowe, token, podlewanie, historyczne dane z sensorów na wykresie z endpointu /api/sensorsdata
export const PlantationCard: React.FC<Props> = ({ title, id }) => {
    const plantationQueryParams = useMemo(() => ({ plantationUUID: id }), [id]);
    const {
        data: plantation,
        isLoading,
        error,
    } = useBackend<PlantationDetails>("/api/plantation", plantationQueryParams);

    return (
        <Card>
            <RemoveButton
                absolute
                onSubmit={() => {
                    globalMutate(
                        "/api/plantation",
                        deleteBackend("/api/plantation", { plantationUUID: id })
                    );
                }}
            />
            <CardContent>
                <Typography variant="h5" component="h2">
                    {title}
                </Typography>
                <Typography sx={{ color: "text.secondary", mb: 4 }}>
                    {plantation?.plant_name}
                </Typography>
                {isLoading && <LinearProgress />}
                {error && "error"}
                {plantation && <AddWaterInfoButton plantationid={id} />}
                {plantation && <PlantationSensors plantationid={id} />}
                {plantation && <GetTokenButton plantationid={plantation.token} />}
            </CardContent>
        </Card>
    );
};

interface SensorProps {
    plantationid: string;
}
const PlantationSensors: React.FC<SensorProps> = ({ plantationid }) => {
    const data = useSensorUpdate(plantationid);
    if (!data) {
        return <CircularProgress />;
    }
    const [wilg, temp, nasl, date] = data;
    return (
        <>
            <Stack direction="row" gap={4}>
                <Typography variant="h5" sx={{color: "#c34e66"}}>
                    <ThermostatIcon /> {temp.toFixed(2)}°C
                </Typography>
                <Typography variant="h5" sx={{color: "skyblue"}}>
                    <OpacityIcon /> {wilg.toFixed(2)}%
                </Typography>
                <Typography variant="h5" sx={{color: "orange"}}>
                    <WbSunnyIcon /> {nasl.toFixed(0)}lx
                </Typography>
            </Stack>
            <Typography variant="caption">
                Zaktualizowano: {date.toLocaleTimeString("pl-PL")}
            </Typography>
        </>
    );
};

const GetTokenButton: React.FC<SensorProps> = ({ plantationid }) => {
    const [isShown, setIsShown] = useState<boolean>(false);
    return (
        <>
            <Button onClick={() => setIsShown(true)} startIcon={<CopyAllIcon />}>
                Pokaż token
            </Button>
            <Dialog open={isShown} onClose={() => setIsShown(false)}>
                <DialogTitle>Skopiuj token do ustawienia na urządzeniu</DialogTitle>
                <DialogContent>
                    <TextField
                        id="outlined-read-only-input"
                        margin="normal"
                        fullWidth
                        label="Token"
                        defaultValue={plantationid}
                        slotProps={{
                            input: {
                                readOnly: true,
                            },
                        }}
                    />
                </DialogContent>
            </Dialog>
        </>
    );
};

const AddWaterInfoButton: React.FC<SensorProps> = ({ plantationid }) => {
    const [isShown, setIsShown] = useState<boolean>(false);

    const onSubmitForm = (e: FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        const data = Object.fromEntries(new FormData(e.nativeEvent.target as any).entries());
        data.wateringTime = String(dayjs(data.wateringTime as string, "DD.MM.YYYY HH:mm").unix);
        console.log(data);
        postBackend("/api/water", data).then(() => setIsShown(false));
    };

    return (
        <>
            <Button
                onClick={() => setIsShown(true)}
                startIcon={<CopyAllIcon />}
                sx={{ float: "right" }}
                variant="contained"
            >
                Zarejestruj podlanie
            </Button>
            <Dialog open={isShown} onClose={() => setIsShown(false)}>
                <form onSubmit={onSubmitForm}>
                    <DialogTitle>Dodaj informacje o podlaniu</DialogTitle>
                    <DialogContent>
                        <input type="hidden" name="plantationUUID" value={plantationid} />
                        <Stack direction="column" gap={4} pt={2}>
                            <DateTimePicker
                                label="czas podlania"
                                name="wateringTime"
                                disableFuture
                                defaultValue={dayjs()}
                            />
                            <TextField
                                label="ilość wody"
                                name="waterAmount"
                                defaultValue={0}
                                type="number"
                                slotProps={{
                                    input: {
                                        endAdornment: (
                                            <InputAdornment position="end">ml</InputAdornment>
                                        ),
                                    },
                                }}
                            />
                        </Stack>
                    </DialogContent>
                    <DialogActions>
                        <Button type="submit" variant="contained" fullWidth>
                            Dodaj
                        </Button>
                    </DialogActions>
                </form>
            </Dialog>
        </>
    );
};
