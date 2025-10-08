#%%
# Preparacion
import matplotlib
# Use a non-interactive backend so scripts can create images without a display
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

#%%
# Carga de la tabla drivers
drivers = pd.read_csv(
    "files/input/drivers.csv",
    sep=",",
    thousands=None,
    decimal=".",
)
drivers.head()

#%%

# Carga de la tabla timesheet
timesheet = pd.read_csv(
    "files/input/timesheet.csv",
    sep=",",
    thousands=None,
    decimal=".",
)
timesheet.head()

#%%

# Media de la cantidad de horas y millas de cada conductor por año
mean_timesheet = timesheet.groupby("driverId").mean()
mean_timesheet.head()

#%%


# Eliminación de la columna 'week'
mean_timesheet.pop("week")
mean_timesheet.head()

#%%

# Registros con valores por debajo de la media del grupo
mean_hours_logged_by_driver = timesheet.groupby("driverId")["hours-logged"].transform(
    "mean"
)
mean_hours_logged_by_driver.head()

#%%

timesheet_with_means = timesheet.copy()
timesheet_with_means["mean_hours-logged"] = mean_hours_logged_by_driver
timesheet_with_means.head()

#%%
# Registros con valores por debajo de la media del grupo (no usar display en
# scripts)
timesheet_below = timesheet_with_means[
    timesheet_with_means["hours-logged"] < timesheet_with_means["mean_hours-logged"]
]
# Note: interactive display() calls were removed because they raise NameError
# when running as a standard Python script. The `timesheet_below` dataframe is
# kept for possible debugging or later use.

#%%

# Cómputo de la cantidad de horas y millas de cada conductor por año
sum_timesheet = timesheet.groupby("driverId").sum()
sum_timesheet.head(10)

#%%

timesheet.groupby("driverId")["hours-logged"].agg([min, max])

#%%

timesheet.groupby("driverId")["hours-logged"].agg([min, max])

#%%

# Unión de las tablas usando join
summary = pd.merge(
    sum_timesheet,
    drivers[["driverId", "name"]],
    on="driverId",
)
summary

#%%

# Almacenamiento de los resultados
import os

if not os.path.exists("files/output"):
    os.makedirs("files/output")

summary.to_csv(
    "files/output/summary.csv",
    sep=",",
    header=True,
    index=False,
)

#%%

# Ordenamiento por la cantidad de millas registradas
top10 = summary.sort_values(by="miles-logged", ascending=False).head(10)
top10

#%%

# Paleta de colores:
#   tab:blue     tab:red       tab:pink
#   tab:orange   tab:purple    tab:gray
#   tab:green    tab:brown     tab:olive
#   tab:cyan
top10["miles-logged"].plot.barh(color="tab:orange", alpha=0.6)

plt.gca().invert_yaxis()

plt.gca().get_xaxis().set_major_formatter(
    matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ","))
)

plt.xticks(rotation=90)

plt.gca().spines["left"].set_color("lightgray")
plt.gca().spines["bottom"].set_color("gray")
plt.gca().spines["top"].set_visible(False)
plt.gca().spines["right"].set_visible(False)

if not os.path.exists("files/plots"):
    os.makedirs("files/plots")

plt.savefig("files/plots/top10_drivers.png", bbox_inches="tight")

#%%