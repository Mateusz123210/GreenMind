"use client";

import { useBackend, useRedirectNotLogged } from "@/services/backend";
import { DerangedSensors, DerangedWeather, Plantation } from "@/types/rest";
import { Box, BoxProps, Card, CardActionArea, CardContent, Collapse, LinearProgress, Stack, styled, Typography } from "@mui/material";
import { useEffect, useMemo, useState } from "react";
import { PlantationChooser } from "@/components/PlantationChooser";
import { DataGrid, GridColDef } from "@mui/x-data-grid";
import dayjs from "dayjs";
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';

interface ExpandMoreProps extends BoxProps {
    expand: boolean;
}

const ExpandMore = styled((props: ExpandMoreProps) => {
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    const { expand, ...other } = props;
    return <Box {...other} />;
})(({ theme }) => ({
    width: 24,
    height: 24,
    transition: theme.transitions.create("transform", {
        duration: theme.transitions.duration.shortest,
    }),
    variants: [
        {
            props: ({ expand }) => !expand,
            style: {
                transform: "rotate(0deg)",
            },
        },
        {
            props: ({ expand }) => !!expand,
            style: {
                transform: "rotate(180deg)",
            },
        },
    ],
}));

export default function Page() {
    useRedirectNotLogged();
    const [isWeatherShown, setIsWeatherShown] = useState<boolean>(false);
    const [isSensorsShown, setIsSensorsShown] = useState<boolean>(false);
    const [chosenPlantation, setChosenPlantation] = useState<Plantation | null>(null);
    const plantation = chosenPlantation?.uuid;
    const plantationQueryParams = useMemo(() => ({ plantationUUID: plantation }), [plantation]);
    const { data: sensorData, isLoading: isSensorsLoading } = useBackend<DerangedSensors>(
        "/api/sensor-data",
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        plantationQueryParams as any,
        !Boolean(chosenPlantation)
    );
    const { data: weatherData, isLoading: isWeatherLoading } = useBackend<DerangedWeather>(
        "/api/weather-data",
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        plantationQueryParams as any,
        !Boolean(chosenPlantation)
    );

    useEffect(() => {
        console.log(sensorData);
        console.log(weatherData);
    }, [sensorData, weatherData]);

    const columnsS: GridColDef[] = [
        { field: "date", headerName: "Data", flex: 1 },
        { field: "tempin", headerName: "Temperatura wewnątrz", flex: 1 },
        { field: "wilgin", headerName: "Wilgotność gleby", flex: 1 },
        { field: "naslin", headerName: "Natężenie oświetlenia", flex: 1 },
    ];

    const columnsW: GridColDef[] = [
        { field: "date", headerName: "Data", flex: 1 },
        { field: "tempout", headerName: "Temperatura na zewnątrz", flex: 1 },
        { field: "wilgout", headerName: "Opady", flex: 1 },
        { field: "uv_index", headerName: "Indeks UV", flex: 1 },
    ]

    const rowsS = sensorData?.sensorsMeasurements.map((sensorEntry, i) => {
        return {
            id: i,
            date: dayjs.unix(sensorEntry[3]).format("YYYY-MM-DDTHH:mm"),
            tempin: sensorEntry[1],
            wilgin: (sensorEntry[0] /110).toPrecision(2) + "%",
            naslin: sensorEntry[2],
        };
    });

    const rowsW = weatherData?.weatherData[0].map((weatherEntry, i) => ({
        id: i,
        date: weatherEntry.time,
        tempout: weatherEntry.temperature,
        wilgout: weatherEntry.precipitation,
        uv_index: weatherEntry.uv_index
    }))

    return (
        <Stack direction="column" gap={4}>
            <PlantationChooser
                plantation={chosenPlantation}
                onPlantationChange={setChosenPlantation}
            />
            {/* <DataGrid
                columns={columns}
                loading={isSensorsLoading || isWeatherLoading}
                rows={rows}
            /> */}
            <Card>
                <CardActionArea onClick={() => setIsWeatherShown((expanded) => !expanded)}>
                    <CardContent>
                        <Stack direction="row" justifyContent="space-between">
                            <Typography gutterBottom variant="h5">
                                Dane pogodowe
                            </Typography>
                            <ExpandMore
                                expand={isWeatherShown}
                                aria-expanded={isWeatherShown}
                                aria-label="show more"
                            >
                                <ExpandMoreIcon />
                            </ExpandMore>
                        </Stack>
                    </CardContent>
                </CardActionArea>
                <Collapse in={isWeatherShown} timeout="auto" unmountOnExit>
                    {(isWeatherLoading || !weatherData) && <LinearProgress />}
                    <CardContent>
                        <DataGrid columns={columnsW} rows={rowsW} loading={isWeatherLoading}/>
                    </CardContent>
                </Collapse>
            </Card>

            <Card>
                <CardActionArea onClick={() => setIsSensorsShown((expanded) => !expanded)}>
                    <CardContent>
                        <Stack direction="row" justifyContent="space-between">
                            <Typography gutterBottom variant="h5">
                                Dane sensorów
                            </Typography>
                            <ExpandMore
                                expand={isSensorsShown}
                                aria-expanded={isSensorsShown}
                                aria-label="show more"
                            >
                                <ExpandMoreIcon />
                            </ExpandMore>
                        </Stack>
                    </CardContent>
                </CardActionArea>
                <Collapse in={isSensorsShown} timeout="auto" unmountOnExit>
                    {(isSensorsLoading || !sensorData) && <LinearProgress />}
                    <CardContent>
                        <DataGrid columns={columnsS} rows={rowsS} loading={isSensorsLoading}/>
                    </CardContent>
                </Collapse>
            </Card>
        </Stack>
    );
}
