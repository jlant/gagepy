# -*- coding: utf-8 -*-

"""
    conftest
    ~~~~~~~~

    Configuration for tests. Contains fixtures, i.e. StringIO representations of
    test data files.

    :copyright: 2015 by Jeremiah Lant, see AUTHORS
    :license: United States Geological Survey (USGS), see LICENSE file
"""

import pytest
import numpy as np
from datetime import datetime, timedelta
from textwrap import dedent


@pytest.fixture(scope="module")
def dates_daily():
    dates = np.array([
            datetime(2015, 8, 1, 0, 0),
            datetime(2015, 8, 2, 0, 0),
            datetime(2015, 8, 3, 0, 0),
            datetime(2015, 8, 4, 0, 0),
            datetime(2015, 8, 5, 0, 0)])

    return dates


@pytest.fixture(scope="module")
def dates_instantaneous():
    dates = np.array([
            datetime(2015, 8, 1, 0, 0),
            datetime(2015, 8, 1, 0, 15),
            datetime(2015, 8, 1, 0, 30),
            datetime(2015, 8, 1, 0, 45),
            datetime(2015, 8, 1, 1, 0)])

    return dates

@pytest.fixture(scope="module")
def dates_and_values():

    dates = np.array([datetime(2015, 1, 1, 0, 0) + timedelta(i) for i in range(11)])
    values = np.array([i for i in range(11)])

    return dates, values


@pytest.fixture(scope="module")
def dates_shorter():

    return np.array([datetime(2015, 1, 3, 0, 0) + timedelta(i) for i in range(11)])


@pytest.fixture(scope="module")
def dates_longer():

    return np.array([datetime(2014, 12, 1, 0, 0) + timedelta(i) for i in range(180)])


@pytest.fixture(scope="module")
def usgs_gage_summary_single_parameter():

    s = dedent(
        """
        Quick Summary
        -------------

        Gage name: {{ name }}
        Start date: {{ start_date }}
        End date: {{ end_date }}
        Number of dates/values: {{ num_vals }}
        Number of parameters: {{ num_params }}

        Parameters
        ----------
        {% for parameter in parameters %}
        {{ parameter.name }} ({{ parameter.units }})
          Mean: {{ parameter.mean() }}
          Max: {{ parameter.max() }} on {{ parameter.max_date() }}
          Min: {{ parameter.min() }} on {{ parameter.min_date() }}
        {% endfor %}

        """
    )


@pytest.fixture(scope="module")
def daily_value_file_single_parameter():
    return \
    """
    # ---------------------------------- WARNING ----------------------------------------
    # The data you have obtained from this automated U.S. Geological Survey database
    # have not received Director"s approval and as such are provisional and subject to
    # revision.  The data are released on the condition that neither the USGS nor the
    # United States Government may be held liable for any damages resulting from its use.
    # Additional info: http://waterdata.usgs.gov/nwis/help/?provisional
    #
    # File-format description:  http://waterdata.usgs.gov/nwis/?tab_delimited_format_info
    # Automated-retrieval info: http://waterdata.usgs.gov/nwis/?automated_retrieval_info
    #
    # Contact:   gs-w_support_nwisweb@usgs.gov
    # retrieved: 2015-08-02 22:08:51 EDT       (sdww01)
    #
    # Data for the following 1 site(s) are contained in this file
    #    USGS 03290500 KENTUCKY RIVER AT LOCK 2 AT LOCKPORT, KY
    # -----------------------------------------------------------------------------------
    #
    # Data provided for site 03290500
    #    DD parameter statistic   Description
    #    06   00060     00003     Discharge, cubic feet per second (Mean)
    #
    # Data-value qualification codes included in this output:
    #     A  Approved for publication -- Processing and review completed.
    #     P  Provisional data subject to revision.
    #     e  Value has been estimated.
    #
    agency_cd	site_no	datetime	06_00060_00003	06_00060_00003_cd
    5s	15s	20d	14n	10s
    USGS	03290500	2015-08-01	100	A
    USGS	03290500	2015-08-02	110	A
    USGS	03290500	2015-08-03	105	A
    USGS	03290500	2015-08-04	107	A
    USGS	03290500	2015-08-05	112	A
    """


@pytest.fixture(scope="module")
def instantaneous_value_file_single_parameter():
    return \
    """
    # ---------------------------------- WARNING ----------------------------------------
    # The data you have obtained from this automated U.S. Geological Survey database
    # have not received Director"s approval and as such are provisional and subject to
    # revision.  The data are released on the condition that neither the USGS nor the
    # United States Government may be held liable for any damages resulting from its use.
    # Additional info: http://nwis.waterdata.usgs.gov/ca/nwis/?provisional
    #
    # File-format description:  http://nwis.waterdata.usgs.gov/nwis/?tab_delimited_format_info
    # Automated-retrieval info: http://nwis.waterdata.usgs.gov/nwis/?automated_retrieval_info
    #
    # Contact:   gs-w_support_nwisweb@usgs.gov
    # retrieved: 2015-08-13 17:19:26 EDT       (nadww01)
    #
    # Data for the following 1 site(s) are contained in this file
    #    USGS 11143000 BIG SUR R NR BIG SUR CA
    # -----------------------------------------------------------------------------------
    #
    # Data provided for site 11143000
    #    DD parameter   Description
    #    03   00065     Gage height, feet
    #
    # Data-value qualification codes included in this output:
    #     A  Approved for publication -- Processing and review completed.
    #     P  Provisional data subject to revision.
    #
    agency_cd	site_no	datetime	tz_cd	03_00065	03_00065_cd
    5s	15s	20d	6s	14n	10s
    USGS	11143000	2015-08-01 00:00	PST	5.0	A
    USGS	11143000	2015-08-01 00:15	PST	10.0	A
    USGS	11143000	2015-08-01 00:30	PST	15.0	A
    USGS	11143000	2015-08-01 00:45	PST	4.5	A
    USGS	11143000	2015-08-01 01:00	PST	5.5	A
    """

@pytest.fixture(scope="module")
def instantaneous_value_file_multi_parameter():
    return \
    """
    # ---------------------------------- WARNING ----------------------------------------
    # The data you have obtained from this automated U.S. Geological Survey database
    # have not received Director"s approval and as such are provisional and subject to
    # revision.  The data are released on the condition that neither the USGS nor the
    # United States Government may be held liable for any damages resulting from its use.
    # Additional info: http://nwis.waterdata.usgs.gov/ky/nwis/?provisional
    #
    # File-format description:  http://nwis.waterdata.usgs.gov/nwis/?tab_delimited_format_info
    # Automated-retrieval info: http://nwis.waterdata.usgs.gov/nwis/?automated_retrieval_info
    #
    # Contact:   gs-w_support_nwisweb@usgs.gov
    # retrieved: 2015-08-11 08:40:40 EDT       (nadww01)
    #
    # Data for the following 1 site(s) are contained in this file
    #    USGS 03401385 DAVIS BRANCH AT HIGHWAY 988 NEAR MIDDLESBORO, KY
    # -----------------------------------------------------------------------------------
    #
    # Data provided for site 03401385
    #    DD parameter   Description
    #    02   00065     Gage height, feet
    #    03   00010     Temperature, water, degrees Celsius
    #    04   00300     Dissolved oxygen, water, unfiltered, milligrams per liter
    #
    # Data-value qualification codes included in this output:
    #     Eqp  Equipment malfunction
    #     P  Provisional data subject to revision.
    #     ~  Value is a system interpolated value.
    #
    agency_cd	site_no	datetime	tz_cd	02_00065	02_00065_cd	03_00010	03_00010_cd	04_00300	04_00300_cd
    5s	15s	20d	6s	14n	10s	14n	10s	14n	10s	14n	10s	14n	10s	14n	10s
    USGS	03401385	2015-08-01 00:00	EDT	1.0	P	5.0	P	2.0	P
    USGS	03401385	2015-08-01 00:15	EDT	2.0	P	10.0	P	1.25	P
    USGS	03401385	2015-08-01 00:30	EDT	3.0	P	15.0	P	1.20	P
    USGS	03401385	2015-08-01 00:45	EDT	4.0	P	20.0	P	0.50	P
    USGS	03401385	2015-08-01 01:00	EDT	5.0	P	25.0	P	0.75	P
    """

@pytest.fixture(scope="module")
def daily_value_file_single_parameter_bad_formatting():
    return \
    """
    # ---------------------------------- WARNING ----------------------------------------
    # The data you have obtained from this automated U.S. Geological Survey database
    # have not received Director"s approval and as such are provisional and subject to
    # revision.  The data are released on the condition that neither the USGS nor the
    # United States Government may be held liable for any damages resulting from its use.
    # Additional info: http://waterdata.usgs.gov/nwis/help/?provisional
    #
    # File-format description:  http://waterdata.usgs.gov/nwis/?tab_delimited_format_info
    # Automated-retrieval info: http://waterdata.usgs.gov/nwis/?automated_retrieval_info
    #
    # Contact:   gs-w_support_nwisweb@usgs.gov
    # retrieved: 2015-08-02 22:08:51 EDT       (sdww01)
    #
    # Data for the following 1 site(s) are contained in this file
    #    USGS 03290500 KENTUCKY RIVER AT LOCK 2 AT LOCKPORT, KY
    # -----------------------------------------------------------------------------------
    #
    # Data provided for site 03290500
    #    DD parameter statistic   Description
    #    06   00060     00003     Discharge, cubic feet per second (Mean)
    #
    # Data-value qualification codes included in this output:
    #     A  Approved for publication -- Processing and review completed.
    #     P  Provisional data subject to revision.
    #     e  Value has been estimated.
    #
    agency_cd	site_no	datetime	06_00060_00003	06_00060_00003_cd
    5s	15s	20d	14n	10s
    USGS	03290500	2015-08-01	10_	A
    USGS	03290500	2015-08-02	20*	A
    USGS	03290500	2015-08-03	$30	A
    USGS	03290500	2015-08-04	#40_	A
    USGS	03290500	2015-08-05	~50&	A
    """

@pytest.fixture(scope="module")
def instantaneous_value_file_single_parameter_missing_data():
    return \
    """
    # ---------------------------------- WARNING ----------------------------------------
    # The data you have obtained from this automated U.S. Geological Survey database
    # have not received Director"s approval and as such are provisional and subject to
    # revision.  The data are released on the condition that neither the USGS nor the
    # United States Government may be held liable for any damages resulting from its use.
    # Additional info: http://nwis.waterdata.usgs.gov/ca/nwis/?provisional
    #
    # File-format description:  http://nwis.waterdata.usgs.gov/nwis/?tab_delimited_format_info
    # Automated-retrieval info: http://nwis.waterdata.usgs.gov/nwis/?automated_retrieval_info
    #
    # Contact:   gs-w_support_nwisweb@usgs.gov
    # retrieved: 2015-08-13 17:19:26 EDT       (nadww01)
    #
    # Data for the following 1 site(s) are contained in this file
    #    USGS 11143000 BIG SUR R NR BIG SUR CA
    # -----------------------------------------------------------------------------------
    #
    # Data provided for site 11143000
    #    DD parameter   Description
    #    03   00065     Gage height, feet
    #
    # Data-value qualification codes included in this output:
    #     A  Approved for publication -- Processing and review completed.
    #     P  Provisional data subject to revision.
    #
    agency_cd	site_no	datetime	tz_cd	03_00065	03_00065_cd
    5s	15s	20d	6s	14n	10s
    USGS	11143000	2015-08-01 00:00	PST	5.0	A
    USGS	11143000	2015-08-01 00:15	PST	10.0	A
    USGS	11143000	2015-08-01 00:30	PST		A
    USGS	11143000	2015-08-01 00:45	PST		A
    USGS	11143000	2015-08-01 01:00	PST	5.5	A
    """

@pytest.fixture(scope="module")
def instantaneous_value_file_single_parameter_bad_characters():
    return \
    """
    # ---------------------------------- WARNING ----------------------------------------
    # The data you have obtained from this automated U.S. Geological Survey database
    # have not received Director"s approval and as such are provisional and subject to
    # revision.  The data are released on the condition that neither the USGS nor the
    # United States Government may be held liable for any damages resulting from its use.
    # Additional info: http://nwis.waterdata.usgs.gov/ca/nwis/?provisional
    #
    # File-format description:  http://nwis.waterdata.usgs.gov/nwis/?tab_delimited_format_info
    # Automated-retrieval info: http://nwis.waterdata.usgs.gov/nwis/?automated_retrieval_info
    #
    # Contact:   gs-w_support_nwisweb@usgs.gov
    # retrieved: 2015-08-13 17:19:26 EDT       (nadww01)
    #
    # Data for the following 1 site(s) are contained in this file
    #    USGS 11143000 BIG SUR R NR BIG SUR CA
    # -----------------------------------------------------------------------------------
    #
    # Data provided for site 11143000
    #    DD parameter   Description
    #    03   00065     Gage height, feet
    #
    # Data-value qualification codes included in this output:
    #     A  Approved for publication -- Processing and review completed.
    #     P  Provisional data subject to revision.
    #
    agency_cd	site_no	datetime	tz_cd	03_00065	03_00065_cd
    5s	15s	20d	6s	14n	10s
    USGS	11143000	2015-08-01 00:00	PST	Ice	A
    USGS	11143000	2015-08-01 00:15	PST	Ice	A
    USGS	11143000	2015-08-01 00:30	PST	*	A
    USGS	11143000	2015-08-01 00:45	PST	*	A
    USGS	11143000	2015-08-01 01:00	PST	50.0	A
    """
